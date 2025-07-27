from datetime import datetime
import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden

# Configure logger to write to requests.log file
logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler('requests.log')
file_handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the current server hour (24-hr format)
        current_hour = datetime.now().hour

        # Only allow access between 6PM (18) and 9PM (21)
        if current_hour < 18 or current_hour > 21:
            return HttpResponseForbidden("Access to chat is only allowed between 6PM and 9PM.")

        response = self.get_response(request)
        return response
    
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = {}  # Stores IP -> [list of datetime objects]

    def __call__(self, request):
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialize list if not exists
            if ip not in self.message_log:
                self.message_log[ip] = []

            # Remove timestamps older than 1 minute
            self.message_log[ip] = [ts for ts in self.message_log[ip] if now - ts < timedelta(minutes=1)]

            # Check limit
            if len(self.message_log[ip]) >= 5:
                return HttpResponseForbidden("Too many messages. Please wait a minute.")

            # Add current timestamp
            self.message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Get IP address even behind a proxy like Nginx."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Example: Check if user is authenticated and has 'role' attribute
        user = getattr(request, 'user', None)
        if user and hasattr(user, 'role'):
            if user.role in ['admin', 'moderator']:
                return self.get_response(request)
            else:
                return HttpResponseForbidden("403 Forbidden: Insufficient permissions")
        else:
            return HttpResponseForbidden("403 Forbidden: Role not found or user not authenticated")