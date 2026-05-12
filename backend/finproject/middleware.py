from django.http import JsonResponse

class HealthCheckMiddleware:
    """
    Intercepts /api/health/ requests before Django's ALLOWED_HOSTS
    check runs, so Kubernetes probes always get a 200 response
    regardless of the pod IP they're coming from.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/api/health/':
            return JsonResponse({'status': 'ok'})
        return self.get_response(request)