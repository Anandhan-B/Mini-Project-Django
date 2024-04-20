class UserLoginDetailsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            if not request.session.get('ip_address'):
                request.session['ip_address'] = request.META.get('REMOTE_ADDR')

        return response
