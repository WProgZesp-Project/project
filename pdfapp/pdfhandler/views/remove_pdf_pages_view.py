from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from PyPDF2 import PdfReader, PdfWriter
from django.shortcuts import render
from ..models import OperationHistory, OperationType
from ..views.operation_history import save_operation
import tempfile
import os


def remove_pdf_pages_view(request):
    return render(request, 'remove_pages.html')


def parse_page_ranges(page_string):
    page_nums = set()
    parts = page_string.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            page_nums.update(range(start - 1, end))
        else:
            page_nums.add(int(part) - 1)
    return page_nums


@csrf_exempt
@require_POST
def remove_pdf_pages(request):
    pdf_file = request.FILES.get('file')
    pages_str = request.POST.get('pages')

    if not pdf_file or not pages_str:
        return JsonResponse(
            {'error': 'PDF file and pages to remove are required.'}, status=400)

    try:
        pages_to_remove = parse_page_ranges(pages_str)
    except Exception:
        return JsonResponse(
            {'error': 'Invalid pages format. Use format like 1,2,4-6.'}, status=400)

    try:
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
        total_pages = len(reader.pages)

        for i in range(total_pages):
            if i not in pages_to_remove:
                writer.add_page(reader.pages[i])

        if len(writer.pages) < 1:
            return JsonResponse(
                {'error': 'Cannot remove all pages from the PDF file.'}, status=400)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_out:
            writer.write(temp_out)
            temp_out_path = temp_out.name
        
        if request.user.is_authenticated:
            save_operation(request, temp_out_path, OperationType.REMOVE_PAGES, [pdf_file.name])


        return FileResponse(
            open(
                temp_out_path,
                'rb'),
            as_attachment=True)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
