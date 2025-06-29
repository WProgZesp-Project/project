import os
from django.shortcuts import render
from django.core.files import File
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..models import OperationHistory, OperationType
from ..serializers.history_serializer import OperationHistorySerializer


# --- Funkcja pomocnicza do zapisu operacji ---
def save_operation(request, file, operation_type, input_filenames, new_filename):
    if request.user.is_authenticated:
        with open(file, 'rb') as f:
            django_file = File(f)
            django_file.name = os.path.basename(new_filename)
            OperationHistory.objects.create(
                user=request.user,
                operation_type=operation_type,
                input_filenames=input_filenames,
                result_file=django_file
            )

# --- Widok HTML ---
def history_page(request):
    return render(request, "history.html")


def history_fragment(request):
    if not request.user.is_authenticated:
        return render(request, "partials/history_fragment.html", {"operations": []})

    operations = OperationHistory.objects.filter(
        user=request.user,
    ).order_by('-created_at')[:5]

    return render(request, "partials/history_fragment.html", {
        "operations": operations
    })


# --- API: GET i POST (plik przez multipart/form-data) ---
class OperationHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        operations = OperationHistory.objects.filter(user=request.user).order_by('-created_at')[:10]
        serializer = OperationHistorySerializer(operations, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id

        # Uwaga: Plik musi być przesłany przez `multipart/form-data`
        serializer = OperationHistorySerializer(data=data, files=request.FILES)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
