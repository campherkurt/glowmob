from admob import set_cookie
from admob import analytics


class AdMobMiddleware(object):
    def process_response(self, request, response):
        """Sets an AdMob cookie if required."""
        if getattr(request, 'has_admob', False):
            response = set_cookie(request, response)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # hack to ignore static file serving
        if hasattr(view_func, '__name__'):
            if not view_func.__name__ == 'serve':
                analytics(request, params=None, fail_silently=True)
                request.has_admob = True
                return view_func(request, *view_args, **view_kwargs)

        return None