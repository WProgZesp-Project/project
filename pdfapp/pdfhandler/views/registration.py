from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..serializers.registration_serializer import UserRegistrationSerializer
import os

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import get_user_model

from .tokens import account_activation_token


class UserRegistrationView(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return render(request, 'registration.html')

    def _activateEmail(self, request, user):
        if os.getenv("TEST") == "true":
            return True

        to_email = user.email
        mail_subject = "Activate your user account."
        protocol = 'https' if request.is_secure() else 'http'
        domain = get_current_site(request).domain
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        message = (
            f"Hi {user.username},\n\n"
            f"Please click the link below to confirm your registration:\n\n"
            f"{protocol}://{domain}/activate/{uid}/{token}"
        )
        email = EmailMessage(mail_subject, message, to=[to_email])
        return email.send()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            if self._activateEmail(request, user):
                user.save()
                if request.headers.get('Hx-Request'):
                    if os.getenv("TEST") == "true":
                        user.is_active = True
                        user.save()
                    # Create response and set header separately (older Django
                    # compatibility)
                    response = HttpResponse(status=200)
                    response['HX-Redirect'] = f"/register/success/?email={user.email}"
                    return response
                return Response(
                    {"message": "User created successfully. Verify your email"},
                    status=status.HTTP_201_CREATED)
            return Response(
                {"message": "Problem with sending verification email"},
                status=status.HTTP_400_BAD_REQUEST)

        errors = serializer.errors
        if request.headers.get('Hx-Request'):
            return render(
                request,
                'partials/registration_errors.html',
                {'errors': errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationSuccessView(View):
    def get(self, request):
        email = request.GET.get('email', '')
        return render(request, 'registration_success.html', {'email': email})


def activate(request, uidb64, token):
    UserModel = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        # Fix: Use UserModel instead of User
        user = UserModel.objects.get(pk=uid)
    except Exception:  # Changed from BaseException for better practice
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(
            request,
            "Thank you for your email confirmation. "
            "Now you can login your account."
        )
        return redirect('http://localhost:8000/')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('http://localhost:8000/')
