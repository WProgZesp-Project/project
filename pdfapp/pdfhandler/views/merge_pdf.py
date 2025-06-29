from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from ..views.operation_history import save_operation, save_operation_temp, OperationType
from PyPDF2 import PdfMerger
import tempfile
import os
from django.conf import settings
import shutil
from django.shortcuts import render
from django.template.loader import render_to_string
import time


@csrf_exempt
@require_POST
def merge_pdfs(request):
    print("Received merge request")
    files = request.FILES.getlist('files')
    order = request.POST.getlist('order')
    print(f"Files received: {[f.name for f in files]}")
    print(f"Order received: {order}")

    if not files or not order or len(files) != len(order):
        print("Files and order are required and must match.")
        return JsonResponse({'error': 'Files and order are required and must match.'}, status=400)

    try:
        ordered_files = [files[int(idx)] for idx in order]
        print(f"Ordered files: {[f.name for f in ordered_files]}")
    except Exception as e:
        print(f"Invalid order indices: {e}")
        return JsonResponse({'error': 'Invalid order indices.'}, status=400)

    merger = PdfMerger()
    filenames = []
    for f in ordered_files:
        print(f"Appending file: {f.name}")
        merger.append(f)
        filenames.append(f.name)

    first_filename = os.path.splitext(filenames[0])[0]

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp:
        merger.write(temp)
        temp_file_path = temp.name
    merger.close()

    if not request.user.is_authenticated:
        s3_path = save_operation_temp(temp_file_path, OperationType.MERGE, filenames)
    else:
        s3_path = save_operation(request, temp_file_path, OperationType.MERGE, filenames)

    html = render_to_string('merge_result_snippet.html', {
        'message': 'PDFs merged successfully!',
        'merged_pdf_url': s3_path
    })

    time.sleep(2)
    return HttpResponse(html)


def merge_form(request):
    return render(request, 'merge.html')


def merge_result(request):
    return render(request, 'merge_result.html')
