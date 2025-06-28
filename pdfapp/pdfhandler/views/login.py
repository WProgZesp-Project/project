from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model, login, authenticate
from ..serializers.login_serializer import UserLoginSerializer

User = get_user_model()

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return render(request, 'login.html')

    def _handle_error_response(self, request, error_message, status_code):
        if request.headers.get('Hx-Request'):
            return HttpResponse(f'<div class="error">{error_message}</div>')
        return Response({"error": error_message}, status=status_code)

    def _handle_success_response(self, request):
        if request.headers.get('Hx-Request'):
            response = HttpResponse(status=200)
            response['HX-Redirect'] = '/'
            return response
        return redirect('/')

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            if request.headers.get('Hx-Request'):
                errors = serializer.errors
                error_html = '<div class="error">'
                if 'email' in errors:
                    error_html += f"Email: {errors['email'][0]}<br>"
                if 'password' in errors:
                    error_html += f"Password: {errors['password'][0]}"
                error_html += '</div>'
                return HttpResponse(error_html)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)

            if not user:
                return self._handle_error_response(
                    request, "Invalid password.", status.HTTP_401_UNAUTHORIZED)

            if not user.is_active:
                return self._handle_error_response(
                    request,
                    "Account is not activated yet. Please check your email and "
                    "click the verification link we sent you.",
                    status.HTTP_403_FORBIDDEN
                )

            login(request, user)
            return self._handle_success_response(request)

        except User.DoesNotExist:
            return self._handle_error_response(
                request, "No user with that email exists.", status.HTTP_401_UNAUTHORIZED)
