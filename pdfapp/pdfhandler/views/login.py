from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model  # Add this line
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
                    return Response(
                        {"error": "Account is not activated yet."},
                        status=status.HTTP_403_FORBIDDEN
                    )
                else:
                    return HttpResponse(status=200)
            else:
                return Response(
                    {"error": "Invalid credentials."},
                    status=status.HTTP_401_UNAUTHORIZED)
