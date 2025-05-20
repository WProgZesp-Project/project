from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from ..serializers.login_serializer import UserLoginSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            from django.contrib.auth import get_user_model

            User = get_user_model()

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user is not None and user.check_password(password):
                if user.is_active:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({
                        'token': token.key,
                        'email': user.email
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Account is not activated yet."}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)