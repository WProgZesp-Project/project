from rest_framework.views import APIView
from django.shortcuts import render
# from rest_framework.permissions import IsAuthenticated


class DashboardView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, 'dashboard.html')
