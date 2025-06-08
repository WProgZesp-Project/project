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
        # render full login page
        return render(request, 'login.html')

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                # First find the user by email
                user_obj = User.objects.get(email=email)
                # Then authenticate with username and password
                user = authenticate(username=user_obj.username, password=password)
                
                if user is not None:
                    if not user.is_active:
                        error_message = "Account is not activated yet."
                        if request.headers.get('Hx-Request'):
                            return HttpResponse(f'<div class="error">{error_message}</div>')
                        return Response(
                            {"error": error_message},
                            status=status.HTTP_403_FORBIDDEN
                        )
                    
                    # User authenticated successfully - log them in
                    login(request, user)
                    
                    # Handle HTMX request
                    if request.headers.get('Hx-Request'):
                        response = HttpResponse(status=200)
                        response['HX-Redirect'] = '/'
                        return response
                    
                    # Handle regular form submission
                    return redirect('/')
                else:
                    # Authentication failed - invalid password
                    error_message = "Invalid password."
                    if request.headers.get('Hx-Request'):
                        return HttpResponse(f'<div class="error">{error_message}</div>')
                    return Response(
                        {"error": error_message},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            except User.DoesNotExist:
                # No user with that email
                error_message = "No user with that email exists."
                if request.headers.get('Hx-Request'):
                    return HttpResponse(f'<div class="error">{error_message}</div>')
                return Response(
                    {"error": error_message},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        # Invalid form data
        if request.headers.get('Hx-Request'):
            errors = serializer.errors
            error_html = '<div class="error">'
            if 'email' in errors:
                error_html += f"Email: {errors['email'][0]}<br>"
            if 'password' in errors:
                error_html += f"Password: {errors['password'][0]}"
            error_html += '</div>'
            return HttpResponse(error_html)
        
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )