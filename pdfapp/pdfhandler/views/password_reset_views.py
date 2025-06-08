from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages
from rest_framework import generics, permissions
from django.http import HttpResponse
import os

from ..serializers.password_reset_serializer import PasswordResetSerializer, SetNewPasswordSerializer
from .tokens import account_activation_token

User = get_user_model()


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return render(request, 'password_reset.html')

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                reset_link = self._send_reset_email(request, user)
                
                is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
                is_htmx = request.headers.get('HX-Request') == 'true'
                test_mode = os.getenv("TEST") == "true"
                
                # Generate the redirect URL
                redirect_url = f"/password-reset/sent/?email={email}"
                if test_mode and reset_link:
                    redirect_url += f"&test_link={reset_link}"
                
                if is_ajax or is_htmx:
                    response = HttpResponse(status=200)
                    response['HX-Redirect'] = redirect_url
                    return response
                return redirect(redirect_url)
                
            except User.DoesNotExist:
                # We don't want to reveal if a user exists, so we still show success
                is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
                is_htmx = request.headers.get('HX-Request') == 'true'
                
                if is_ajax or is_htmx:
                    response = HttpResponse(status=200)
                    response['HX-Redirect'] = f"/password-reset/sent/?email={email}"
                    return response
                return redirect('password_reset_sent', email=email)
        
        # Handle errors
        errors = serializer.errors
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        is_htmx = request.headers.get('HX-Request') == 'true'
        
        if is_ajax or is_htmx:
            error_html = "<ul class='error'>"
            for field in errors:
                for error in errors[field]:
                    error_html += f"<li>{field}: {error}</li>"
            error_html += "</ul>"
            return HttpResponse(error_html)
        
        return render(request, 'password_reset.html', {'errors': errors})

    def _send_reset_email(self, request, user):
        to_email = user.email
        mail_subject = "Reset your password"
        protocol = 'https' if request.is_secure() else 'http'
        domain = get_current_site(request).domain
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        reset_link = f"{protocol}://{domain}/password-reset/confirm/{uid}/{token}/"
        message = (
            f"Hi {user.username},\n\n"
            f"Please click the link below to reset your password:\n\n"
            f"{reset_link}"
        )
        email = EmailMessage(mail_subject, message, to=[to_email])
        
        if os.getenv("TEST") == "true":
            print(f"[TEST MODE] Reset link would be sent to {to_email}: {reset_link}")
            return reset_link
        
        try:
            result = email.send()
            print(f"Password reset email sent to {to_email}: {result == 1}")
            return reset_link if result == 1 else None
        except Exception as e:
            print(f"Error sending password reset email to {to_email}: {str(e)}")
            return None


class PasswordResetSentView(View):
    def get(self, request):
        email = request.GET.get('email', '')
        test_link = request.GET.get('test_link', '')
        test_mode = os.getenv("TEST") == "true"
        return render(request, 'password_reset_sent.html', {
            'email': email,
            'test_link': test_link,
            'test_mode': test_mode
        })


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            if not account_activation_token.check_token(user, token):
                messages.error(request, "Password reset link is invalid or has expired!")
                return redirect('login')
                
            return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
        
        except Exception:
            messages.error(request, "Password reset link is invalid or has expired!")
            return redirect('login')

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            if not account_activation_token.check_token(user, token):
                messages.error(request, "Password reset link is invalid!")
                return redirect('login')
            
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                password = serializer.validated_data['password']
                user.set_password(password)
                user.save()
                messages.success(request, "Your password has been changed successfully!")
                return redirect('password_reset_complete')
            
            return render(request, 'password_reset_confirm.html', {
                'errors': serializer.errors,
                'uidb64': uidb64,
                'token': token
            })
            
        except Exception:
            messages.error(request, "Password reset link is invalid!")
            return redirect('login')


class PasswordResetCompleteView(View):
    def get(self, request):
        return render(request, 'password_reset_complete.html')