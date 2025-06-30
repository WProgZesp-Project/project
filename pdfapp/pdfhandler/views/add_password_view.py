from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
from PyPDF2 import PdfReader, PdfWriter
from ..views.operation_history import save_operation, save_operation_temp, OperationType
import tempfile


def add_password_page(request):
    return render(request, 'add_password.html')


def lock_pdf_file(pdf_file, password):
    try:
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(password)
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
def add_pdf_password(request):
    pdf_file = request.FILES.get('file')
    password = request.POST.get('password')

    if not pdf_file or not password:
        return JsonResponse(
            {'error': 'File and password are required.'}, status=400)
    temp_out_path, error = lock_pdf_file(pdf_file, password)

    if error:
        return JsonResponse({'error': error}, status=400)

    if request.user.is_authenticated:
        save_operation(request, temp_out_path, OperationType.ADD_PASSWORD, [pdf_file.name])
    else:
        save_operation_temp(temp_out_path, OperationType.ADD_PASSWORD, [pdf_file.name])

    response = FileResponse(
        open(
            temp_out_path,
            'rb'),
        as_attachment=True)
    return response 