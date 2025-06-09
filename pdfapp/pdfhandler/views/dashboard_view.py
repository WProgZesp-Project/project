from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json


class DashboardView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = []

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            username = mark_safe(json.dumps(user.username))
            return render(request, 'dashboard.html', {'username': username, 'authenticated': True})
        else:
            return render(request, 'dashboard.html', {'authenticated': False})
