from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
from PyPDF2 import PdfReader, PdfWriter
from ..models import OperationHistory, OperationType
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


def validate_pdf_and_pages(pdf_file, pages_str):
    if not pdf_file or not pages_str:
        return None, None, JsonResponse(
            {'error': 'PDF file and pages to remove are required.'}, status=400)
    try:
        reader = PdfReader(pdf_file)
        total_pages = len(reader.pages)
        return reader, total_pages, None
    except Exception:
        return None, None, JsonResponse({'error': 'Failed to read PDF file.'}, status=400)


def validate_page_numbers(pages_str, total_pages):
    try:
        raw_pages = parse_page_ranges(pages_str)
    except Exception:
        return None, JsonResponse({
            'error': 'Invalid pages format. Use format like 1,2,4-6.'
        }, status=400)

    valid_pages = set()
    for p in raw_pages:
        if not isinstance(p, int) or p < 0 or p >= total_pages:
            return None, JsonResponse({
                'error': f'Page number {p + 1} is out of range. PDF has {total_pages} pages.'
            }, status=400)
        valid_pages.add(p)

    if len(valid_pages) >= total_pages:
        return None, JsonResponse({
            'error': 'Cannot remove all pages from the PDF file.'
        }, status=400)

    return valid_pages, None


@csrf_exempt
@require_POST
def remove_pdf_pages(request):
    pdf_file = request.FILES.get('file')
    pages_str = request.POST.get('pages')

    reader, total_pages, error = validate_pdf_and_pages(pdf_file, pages_str)
    if error:
        return error

    pages_to_remove, error = validate_page_numbers(pages_str, total_pages)
    if error:
        return error

    writer = PdfWriter()
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
        OperationHistory.objects.create(
            user=request.user,
            operation_type=OperationType.REMOVE_PAGES,
            input_filenames=[pdf_file.name],
            result_filename=os.path.basename(temp_out_path)
        )

    filename = f'{os.path.splitext(pdf_file.name)[0]} (removed-pages).pdf'
    return FileResponse(
        open(temp_out_path, 'rb'),
        as_attachment=True,
        filename=filename
    )
