from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from PyPDF2 import PdfMerger
from ..models import OperationHistory, OperationType
import tempfile
import os


@csrf_exempt
@require_POST
def merge_pdfs(request):
    files = request.FILES.getlist('files')
    order = request.POST.getlist('order')  # List of indices as strings
    if not files or not order or len(files) != len(order):
        return JsonResponse(
            {'error': 'Files and order are required and must match.'},
            status=400)

    # Reorder files according to user-specified order
    try:
        ordered_files = [files[int(idx)] for idx in order]
    except Exception:
        return JsonResponse({'error': 'Invalid order indices.'}, status=400)

    merger = PdfMerger()
    filenames = []
    for f in ordered_files:
        merger.append(f)
        filenames.append(f.name)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_out:
        merger.write(temp_out)
        merged_filename = os.path.basename(temp_out.name)
        temp_out_path = temp_out.name

    # Save history if user is logged in
    if request.user.is_authenticated:
        OperationHistory.objects.create(
            user = request.user,
            operation_type=OperationType.MERGE,
            input_filenames=filenames,
            result_filename=merged_filename
        )

    response = FileResponse(
        open(
            temp_out_path,
            'rb'),
        as_attachment=True,
        filename='merged.pdf')
    return response
