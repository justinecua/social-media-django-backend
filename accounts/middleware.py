

class JWTTokenCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("🧠 Middleware hit!")
        access_token = request.COOKIES.get("access_token")
        print("🔐 access_token from cookie:", access_token)

        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
            print("✅ Injected Authorization header")

        return self.get_response(request)
