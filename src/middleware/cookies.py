
class UpdateCookiesMiddleware(object):
    
    def process_response(self, request, response):
        #request.session['cookies'] = None
        try:
            if request._cookies:
               for k, v in request._cookies.items():
                   response.set_cookie(k, v)
        except AttributeError:
           pass
       
        return response