from django.http import Http404
from functools import wraps

def admin_role_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Admin':  
            return view_func(request, *args, **kwargs)
        else:
            raise Http404("Page not found")
    return _wrapped_view

def both_role_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Admin' or request.user.role == 'Editor':
            return view_func(request, *args, **kwargs)
        else:
            raise Http404("Page not fount")
    return _wrapped_view