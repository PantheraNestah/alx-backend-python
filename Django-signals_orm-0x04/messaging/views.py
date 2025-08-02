from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .models import Message, MessageHistory
from django.db.models import Q

def message_detail(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    # Prefetch edit history with the editors to avoid N+1 queries
    edit_history = message.history.select_related('edited_by').all()
    
    return render(request, 'messaging/message_details.html', {
        'message': message,
        'edit_history': edit_history,
    })

@login_required
def delete_user_account(request):
    if request.method == 'POST':
        user = request.user
        # Log the user out before deleting their account
        logout(request)
        # Delete the user object, which will trigger the signal
        user.delete()
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home') # Redirect to a home page or another appropriate page

    return render(request, 'messaging/delete_account_confirm.html')

@login_required
@cache_page(60) # Cache this view for 60 seconds
def conversation_thread_view(request, message_id):
    # Find the root message of the thread
    try:
        current_message = Message.objects.select_related('parent_message').get(pk=message_id)
        root_message = current_message
        while root_message.parent_message:
            root_message = root_message.parent_message
    except Message.DoesNotExist:
        return render(request, '404.html') # Or some error page

    # Now that we have the root, we need to fetch all its descendants.
    # A raw SQL query with a recursive Common Table Expression (CTE) is the most performant way.
    
    raw_query = """
    WITH RECURSIVE message_thread AS (
        -- Base case: select the root message
        SELECT * FROM messaging_message WHERE id = %s
        UNION ALL
        -- Recursive step: select all replies
        SELECT m.* FROM messaging_message m
        JOIN message_thread mt ON m.parent_message_id = mt.id
    )
    SELECT * FROM message_thread;
    """
    
    # Execute the raw query and prefetch related users
    all_messages_in_thread = list(Message.objects.raw(raw_query, [root_message.id]))
    
    # Manually prefetch sender and receiver to avoid N+1 in the template
    user_ids = {msg.sender_id for msg in all_messages_in_thread} | {msg.receiver_id for msg in all_messages_in_thread}
    users_by_id = {user.id: user for user in User.objects.filter(id__in=user_ids)}

    # Build the thread structure in Python
    messages_by_id = {}
    for msg in all_messages_in_thread:
        # Attach the prefetched user objects
        msg.sender = users_by_id.get(msg.sender_id)
        msg.receiver = users_by_id.get(msg.receiver_id)
        # Initialize an empty list for replies
        msg.threaded_replies = []
        messages_by_id[msg.id] = msg

    # Link replies to their parents
    for msg in all_messages_in_thread:
        if msg.parent_message_id and msg.parent_message_id in messages_by_id:
            parent = messages_by_id[msg.parent_message_id]
            parent.threaded_replies.append(msg)

    # The final result is the root message with all children nested within it
    thread_root_with_replies = messages_by_id[root_message.id]
    
    return render(request, 'messaging/conversation_thread.html', {
        'root_message': thread_root_with_replies,
    })

@login_required
def inbox_view(request):
    # Use our custom manager to get the unread messages
    unread_messages = Message.unread.unread_for_user(request.user)
    
    # For demonstration, let's also have a way to mark a message as read
    message_to_mark_read_id = request.GET.get('mark_read')
    if message_to_mark_read_id:
        try:
            message = Message.objects.get(pk=message_to_mark_read_id, receiver=request.user)
            message.is_read = True
            message.save()
            return redirect('inbox') # Redirect to refresh the list
        except Message.DoesNotExist:
            # Handle error: message not found or doesn't belong to the user
            pass

    return render(request, 'messaging/inbox.html', {
        'unread_messages': unread_messages,
    })

@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    
    # Only the sender can edit their own messages
    if message.sender != request.user:
        return HttpResponseForbidden("You can only edit your own messages.")
    
    if request.method == 'POST':
        new_content = request.POST.get('content', '').strip()
        if new_content and new_content != message.content:
            # Set the editor information before saving
            message._edited_by = request.user
            message.content = new_content
            message.save()
            messages.success(request, 'Message updated successfully!')
            return redirect('message_detail', message_id=message.id)
    
    return render(request, 'messaging/edit_message.html', {
        'message': message,
    })
