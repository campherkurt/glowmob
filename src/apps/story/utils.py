from django.core.cache import cache

def cache_page_with_dynamic_key(*cache_args):
    """
    A cache decorator that will allow you to dynamically set
    with which key and for how long the HttpResponse should be stored.
    
    def my_key_callback(request):
        # cache for 60 seconds with a cache key that looks like:
        #  username@/my/app/view?key=value
        return 60, "%s@%s?%s" % (
            request.user.username, 
            request.path, 
            request.META.get('QUERY_STRING')
        )
    
    @cache_page_with_dynamic_key(my_key_callback)
    def myview(request, *args, **kwargs):
        # do some heavy calculation
        return HttpResponse("42")
    
    """
    def _decorator(view):
        def _wrapped_view(request, *args, **kwargs):
            # Only check for GETs
            if request.method == 'GET':
                # if we've been given two arguments assume they're the key and the timeout
                if len(cache_args) == 2:
                    cache_timeout, cache_key = cache_args
                # otherwise we're assuming that it's a callable that will
                # return us the timeout and key as a tuple
                elif len(cache_args) == 1 and callable(cache_args[0]):
                    cache_timeout, cache_key = cache_args[0](request)
                # hopeless...
                else:
                    raise Exception, "Provide either the timeout and key, or a callable"
                
                response = cache.get(cache_key)
                # if not, have the view function process it and cache the results
                if response is None:
                    response = view(request, *args, **kwargs)
                    # only cache responses that have an HTTP 2xx status code
                    if 200 <= response.status_code < 300:
                        cache.set(cache_key, response, cache_timeout)
                # return the cached value
                return response
            else:
                return view(request, *args, **kwargs)
        return _wrapped_view
    return _decorator

