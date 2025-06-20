from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token


class LogoutView(View):
    @method_decorator(csrf_protect)
    def post(self, request):
        # Clean up token if exists
        if hasattr(request.user, 'auth_token'):
            try:
                request.user.auth_token.delete()
            except (AttributeError, Token.DoesNotExist):
                pass
        
        # Perform Django session logout
        logout(request)
        
        # Redirect to home page
        return redirect('index')