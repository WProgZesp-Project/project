class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('auth_token')
        if token:
            request.META['HTTP_AUTHORIZATION'] = f'Token {token}'
        return self.get_response(request)
