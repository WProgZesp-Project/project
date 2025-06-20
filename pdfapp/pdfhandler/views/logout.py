from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token

class UserLogoutView(View):  # Renamed to UserLogoutView
    @method_decorator(csrf_protect)
    def post(self, request):
        if hasattr(request.user, 'auth_token'):
            try:
                request.user.auth_token.delete()
            except (AttributeError, Token.DoesNotExist):
                pass
        logout(request)
        return redirect('index')