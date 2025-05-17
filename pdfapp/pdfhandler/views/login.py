from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from ..serializers.login_serializer import UserLoginSerializer

User = get_user_model()

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # render full login page
        return render(request, 'login.html')

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user and user.check_password(password):
                if not user.is_active:
                    error = "Account is not activated yet."
                    status_code = status.HTTP_403_FORBIDDEN
                else:
                    # successful login → HTMX redirect
                    if request.headers.get('Hx-Request'):
                        return HttpResponse(
                            status=200,
                            headers={'HX-Redirect': '/'}
                        )
                    return redirect('index')
            else:
                error = "Invalid credentials."
                status_code = status.HTTP_401_UNAUTHORIZED
        else:
            error = "Invalid credentials."
            status_code = status.HTTP_401_UNAUTHORIZED

        # failure: return HTML fragment with error
        if request.headers.get('Hx-Request'):
            return render(
                request,
                'partials/login_errors.html',
                {'error': error},
                status=status_code
            )
        # non-HTMX fallback
        return render(request, 'login.html', {'error': error})