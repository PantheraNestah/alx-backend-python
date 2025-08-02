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
    # Find the root message of the thread using optimized query
    try:
        current_message = Message.objects.select_related('parent_message', 'sender', 'receiver').get(pk=message_id)
        root_message = current_message
        while root_message.parent_message:
            root_message = root_message.parent_message
    except Message.DoesNotExist:
        return render(request, '404.html') # Or some error page

    # Use Django ORM recursive query to fetch all replies to a message
    def get_message_thread_recursive(root_msg):
        """
        Recursive function using Django's ORM to fetch all replies to a message 
        and display them in a threaded format.
        """
        # Get direct replies using Message.objects.filter with optimizations
        direct_replies = Message.objects.filter(
            parent_message=root_msg
        ).select_related(
            'sender', 'receiver', 'parent_message'
        ).prefetch_related(
            'history__edited_by', 'replies__sender', 'replies__receiver'
        ).order_by('timestamp')
        
        # Recursively get replies for each direct reply
        for reply in direct_replies:
            reply.threaded_replies = get_message_thread_recursive(reply)
        
        return list(direct_replies)
    
    # Get the complete thread structure starting from root
    root_message.threaded_replies = get_message_thread_recursive(root_message)
    
    return render(request, 'messaging/conversation_thread.html', {
        'root_message': root_message,
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

@login_required
def sent_messages_view(request):
    """
    View to show messages sent by the current user with optimized queries.
    """
    # Use Message.objects.filter with sender=request.user and optimize with select_related
    sent_messages = Message.objects.filter(
        sender=request.user
    ).select_related(
        'receiver', 'parent_message'
    ).prefetch_related(
        'history__edited_by', 'replies__sender', 'replies__receiver'
    ).order_by('-timestamp')
    
    return render(request, 'messaging/sent_messages.html', {
        'sent_messages': sent_messages,
    })

@login_required
def user_conversations_view(request):
    """
    View to show all conversations involving the current user with query optimization.
    """
    # Use Message.objects.filter to get messages where user is sender or receiver
    user_messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related(
        'sender', 'receiver', 'parent_message'
    ).prefetch_related(
        'replies__sender', 'replies__receiver', 'history__edited_by'
    ).order_by('-timestamp')
    
    return render(request, 'messaging/conversations.html', {
        'user_messages': user_messages,
    })
