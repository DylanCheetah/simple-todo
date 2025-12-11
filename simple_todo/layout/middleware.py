from django.http import QueryDict
from django.utils.deprecation import MiddlewareMixin


# Middleware Classes
# ==================
class HttpPutMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # If the request is an HTTP PUT request, parse the submitted form data
        if request.method == "PUT":
            request.POST = QueryDict(request.body)
