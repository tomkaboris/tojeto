from django.http import HttpResponseForbidden
from django.conf import settings


class RestrictModeratorIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path starts with '/moderator/'
        if request.path.startswith('/moderator/'):
            # Get the client's IP address
            ip_address = request.META.get('REMOTE_ADDR')

            # Allow access only if the IP is in the allowed list
            allowed_ips = getattr(settings, 'ALLOWED_MODERATOR_IPS', [])
            if ip_address not in allowed_ips:
                return HttpResponseForbidden("Access restricted to this page.")
        
        # Continue processing the request
        return self.get_response(request)
