import logging
from datetime import datetime

# Get an instance of the 'request_logger' logger
logger = logging.getLogger('request_logger')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        
        # Use the logger to log the message
        log_message = f"User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)

        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view is called.
        """
        # We will assume the chat application's URLs start with '/chat/'
        # This prevents the middleware from blocking the entire site (e.g., admin panel).
        if request.path.startswith('/chat/'):
            current_hour = datetime.now().hour
            
            # The allowed hours are from 6 AM (6) up to 9 PM (21).
            # So, we deny access if the hour is NOT in this range.
            if not (6 <= current_hour < 21):
                return HttpResponseForbidden("<h1>Access Denied</h1><p>The chat is only available between 6 AM and 9 PM.</p>")

        # If the time is valid or the path is not for the chat, continue to the view.
        response = self.get_response(request)
        
        # Code to be executed for each request/response after the view is called.
        return response


class OffensiveLanguageMiddleware:
    # Store request records in a dictionary: {'ip_address': [timestamp1, timestamp2, ...]}
    request_records = {}
    
    # --- Configuration ---
    TIME_WINDOW_SECONDS = 60  # 1 minute
    REQUEST_LIMIT = 5         # 5 messages per minute

    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        This method is called for every request.
        """
        # We only want to rate-limit POST requests to a chat submission URL.
        # IMPORTANT: Adjust '/chat/send-message/' to your actual message submission URL.
        if request.method == 'POST' and request.path.startswith('/chat/send-message/'):
            ip_address = self.get_client_ip(request)
            current_time = time.time()

            # Get or initialize the list of timestamps for this IP
            timestamps = self.request_records.get(ip_address, [])

            # Filter out timestamps that are outside our time window
            recent_timestamps = [ts for ts in timestamps if ts > current_time - self.TIME_WINDOW_SECONDS]

            # Check if the user has exceeded the limit
            if len(recent_timestamps) >= self.REQUEST_LIMIT:
                # Return a JSON response for API-like endpoints or a standard HTML response
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                     return JsonResponse(
                        {"error": "Too many requests. Please wait a moment."},
                        status=429 # Status code for "Too Many Requests"
                    )
                return HttpResponseForbidden("<h1>Rate Limit Exceeded</h1><p>You are sending messages too quickly. Please wait a moment.</p>")

            # Add the current request's timestamp and update the record
            recent_timestamps.append(current_time)
            self.request_records[ip_address] = recent_timestamps

        # If the limit is not exceeded, or the request is not a chat message, proceed as normal.
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """
        Get the client's real IP address from the request.
        """
        # This handles standard setups and proxies that set the 'X-Forwarded-For' header.
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolePermissionMiddleware:
    # --- Configuration ---
    # Define URL path prefixes that require special permissions.
    # Any URL starting with these will be checked.
    PROTECTED_PATHS = ['/management/', '/dashboard/']

    # Define the roles that are allowed to access the protected paths.
    ALLOWED_ROLES = ['admin', 'moderator']

    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        This method is called for every request.
        """
        # Check if the requested path is one of the protected paths.
        is_protected_path = any(request.path.startswith(path) for path in self.PROTECTED_PATHS)

        if is_protected_path:
            # First, check if the user is authenticated at all.
            if not request.user.is_authenticated:
                return HttpResponseForbidden("<h1>Access Denied</h1><p>You must be logged in to view this page.</p>")

            # Check if the user has a 'role' attribute.
            # This is based on the assumption you have a custom user model or profile with this attribute.
            user_role = getattr(request.user, 'role', None)

            # If the user's role is not in the allowed list, deny access.
            if user_role not in self.ALLOWED_ROLES:
                return HttpResponseForbidden("<h1>Permission Denied</h1><p>You do not have the required permissions to access this page.</p>")

        # If the path isn't protected or the user has the correct role, proceed as normal.
        response = self.get_response(request)
        return response