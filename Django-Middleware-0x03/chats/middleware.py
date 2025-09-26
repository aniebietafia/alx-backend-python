import logging
from datetime import datetime

from django.http import JsonResponse

# Configure logger with more specific settings
logger = logging.getLogger('request_logging')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('request.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Basic configuration for logging to a file
logging.basicConfig(filename='request.log', level=logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        user = request.user.email if request.user.is_authenticated else 'AnonymousUser'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

        response = self.get_response(request)

        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for chat-related paths
        if self.is_chat_request(request):
            current_hour = datetime.now().hour

            # Check if current time is outside allowed hours (6PM to 9PM = 18 to 21)
            if current_hour < 18 or current_hour >= 21:
                return JsonResponse(
                    {'error': 'Chat access is restricted. Available from 6:00 PM to 9:00 PM.'},
                    status=403
                )

        response = self.get_response(request)
        return response

    def is_chat_request(self, request):
        """
        Check if the request is related to chat functionality.
        Adjust paths based on your URL patterns.
        """
        chat_paths = ['/api/conversations/', '/api/messages/']
        return any(request.path.startswith(path) for path in chat_paths)

