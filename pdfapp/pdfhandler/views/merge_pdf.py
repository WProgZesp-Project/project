from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from ..views.operation_history import save_operation, OperationType
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

    temp_dir = tempfile.mkdtemp()
    first_filename = os.path.splitext(filenames[0])[0]
    merged_filename = f'merge_{first_filename}.pdf'
    temp_out_path = os.path.join(temp_dir, merged_filename)
    print(f"Writing merged PDF to: {temp_out_path}")
    merger.write(temp_out_path)
    merger.close()

    if request.user.is_authenticated:
        save_operation(request, temp_out_path, OperationType.MERGE, filenames)

    final_path = os.path.join(settings.MEDIA_ROOT, merged_filename)
    print(f"Moving merged PDF to: {final_path}")
    shutil.move(temp_out_path, final_path)

    shutil.rmtree(temp_dir)
    print("Temporary directory cleaned up.")

    merged_pdf_url = settings.MEDIA_URL + merged_filename
    print(f"Merging complete. File available at: {merged_pdf_url}")

    html = render_to_string('merge_result_snippet.html', {
        'message': 'PDFs merged successfully!',
        'merged_pdf_url': merged_pdf_url
    })


    time.sleep(2)
    return HttpResponse(html)


def merge_form(request):
    return render(request, 'merge.html')


def merge_result(request):
    return render(request, 'merge_result.html')
