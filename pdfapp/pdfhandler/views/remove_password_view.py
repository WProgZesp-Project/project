from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
from PyPDF2 import PdfReader, PdfWriter
from ..models import OperationHistory, OperationType
from ..views.operation_history import save_operation, OperationType
import tempfile
import os


def remove_password_page(request):
    return render(request, 'remove_password.html')


def unlock_pdf_file(pdf_file, password):
    try:
        reader = PdfReader(pdf_file)
        if reader.is_encrypted:
            if not reader.decrypt(password):
                return None, 'Incorrect password.'
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        with tempfile.NamedTemporaryFile(
            delete=False, suffix='.pdf'
        ) as temp_out:
            writer.write(temp_out)
            temp_out_path = temp_out.name
        return temp_out_path, None
    except Exception as e:
        msg = 'Failed to process PDF: {0}'.format(str(e))
        return None, msg


@csrf_exempt
@require_POST
def remove_pdf_password(request):
    pdf_file = request.FILES.get('file')
    password = request.POST.get('password')

    if not pdf_file or not password:
        return JsonResponse(
            {'error': 'File and password are required.'}, status=400)
    temp_out_path, error = unlock_pdf_file(pdf_file, password)

    if error:
        return JsonResponse({'error': error}, status=400)

    if request.user.is_authenticated:
        save_operation(request, temp_out_path, OperationType.REMOVE_PASSWORD, [pdf_file.name])

    response = FileResponse(
        open(
            temp_out_path,
            'rb'),
        as_attachment=True,
        filename='unlocked.pdf')
    return response
