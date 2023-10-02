import socket
from django.core.exceptions import RequestTimeout

from django.utils import timezone
import pytz


class RequestTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set the timeout duration in seconds
        timeout = 360

        # Set the timeout for the current request
        socket.setdefaulttimeout(timeout)

        try:
            return self.get_response(request)
        except socket.timeout:
            raise RequestTimeout


class TimeZoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timezone.activate(pytz.timezone('Asia/Kolkata'))

        response = self.get_response(request)

        timezone.deactivate()

        return response
