from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..serializers.registration_serializer import UserRegistrationSerializer
import os

from django.shortcuts import render, redirect
from django.http import JsonResponse
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
        to_email = user.email
        mail_subject = "Activate your user account."
        protocol = 'https' if request.is_secure() else 'http'
        domain = get_current_site(request).domain
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        activation_link = f"{protocol}://{domain}/activate/{uid}/{token}"
        message = (
            f"Hi {user.username},\n\n"
            f"Please click the link below to confirm your registration:\n\n"
            f"{activation_link}"
        )
        email = EmailMessage(mail_subject, message, to=[to_email])
        
        if os.getenv("TEST") == "true":
            print(f"[TEST MODE] Activation link would be sent to {to_email}: {activation_link}")
            user.is_active = True
            return activation_link
        
        try:
            result = email.send()
            print(f"Activation email sent to {to_email}: {result == 1}")
            return activation_link if result == 1 else None
        except Exception as e:
            print(f"Error sending activation email to {to_email}: {str(e)}")
            return None

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            activation_link = self._activateEmail(request, user)
            user.save()
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            is_htmx = request.headers.get('HX-Request') == 'true'
            test_mode = os.getenv("TEST") == "true"
            
            redirect_url = f"/register/success/?email={user.email}"
            if test_mode and activation_link:
                redirect_url += f"&test_link={activation_link}"
            
            if is_ajax or is_htmx:
                response = JsonResponse({"message": "User created successfully."}, status=201)
                response['HX-Redirect'] = redirect_url
                return response
            
            return redirect(redirect_url)
            
        errors = serializer.errors
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        is_htmx = request.headers.get('HX-Request') == 'true'
        
        if is_ajax or is_htmx:
            return JsonResponse(errors, status=400)
        
        return render(request, 'registration.html', {'errors': errors}, status=400)


class RegistrationSuccessView(View):
    def get(self, request):
        email = request.GET.get('email', '')
        test_link = request.GET.get('test_link', '')
        test_mode = os.getenv("TEST") == "true"
        return render(request, 'registration_success.html', {
            'email': email,
            'test_link': test_link,
            'test_mode': test_mode
        })


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