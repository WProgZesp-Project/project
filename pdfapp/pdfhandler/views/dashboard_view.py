from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render

class DashboardView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, 'dashboard.html')