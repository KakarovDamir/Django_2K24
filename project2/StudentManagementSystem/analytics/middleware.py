from django.utils.deprecation import MiddlewareMixin
from .models import APIRequestLog

class APILoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            APIRequestLog.objects.create(
                user=request.user,
                path=request.path,
                method=request.method
            )

