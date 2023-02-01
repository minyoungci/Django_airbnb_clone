from rest_framework.authentication import BaseAuthentication


class TrustMeBroAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print(request.headers)
        return None
