from django.shortcuts import redirect
from functools import wraps


def check_display_name(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or bool(getattr(request.user, 'display_name', False)):
            return view_func(request, *args, **kwargs)
        return redirect("set-display-name")
    return wrapper
