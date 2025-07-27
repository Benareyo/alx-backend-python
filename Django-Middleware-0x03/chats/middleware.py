from datetime import datetime
import logging
from datetime import datetime
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
