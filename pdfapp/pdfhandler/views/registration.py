from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..serializers.registration_serializer import UserRegistrationSerializer
import os
import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
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
        # If TEST mode is enabled, skip email sending and activate user directly
        if os.getenv("TEST") == "true":
            user.is_active = True
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
            
            # Attempt to send activation email or activate directly in TEST mode
            if self._activateEmail(request, user):
                # Save the user (now with is_active=True if in TEST mode)
                user.save()
                
                # Handle HTMX or XMLHttpRequest
                is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
                is_htmx = request.headers.get('HX-Request') == 'true'
                
                if is_ajax or is_htmx:
                    response = JsonResponse({"message": "User created successfully."}, status=201)
                    response['HX-Redirect'] = f"/register/success/?email={user.email}"
                    return response
                
                # For regular form submission
                return redirect('registration_success', email=user.email)
            
            # If activation email failed
            return Response(
                {"message": "Problem with sending verification email"},
                status=status.HTTP_400_BAD_REQUEST)

        # Handle errors - important fix here
        errors = serializer.errors
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        is_htmx = request.headers.get('HX-Request') == 'true'
        
        if is_ajax or is_htmx:
            # Return errors as JSON with 400 status code
            return JsonResponse(errors, status=400)
        
        # For regular form submission
        return render(request, 'registration.html', {'errors': errors}, status=400)


class RegistrationSuccessView(View):
    def get(self, request):
        email = request.GET.get('email', '')
        return render(request, 'registration_success.html', {'email': email})


def activate(request, uidb64, token):
    UserModel = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(
            request,
            "Thank you for your email confirmation. Now you can login your account."
        )
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('index')