from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
from ..models import OperationType
from ..views.operation_history import save_operation, save_operation_temp
from PyPDF2 import PdfReader, PdfWriter
import tempfile


def remove_pdf_pages_view(request):
    return render(request, 'remove_pages.html')


def parse_page_ranges(pages_str, total_pages):
    pages_to_remove = set()
    for part in pages_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            start = max(1, start)
            end = min(total_pages, end)
            pages_to_remove.update(range(start - 1, end))
        else:
            page = int(part) - 1
            if 0 <= page < total_pages:
                pages_to_remove.add(page)
    return pages_to_remove


def validate_pdf_and_pages(pdf_file, pages_str):
    if not pdf_file or not pages_str:
        return None, None, JsonResponse({'error': 'PDF file and pages to remove are required.'}, status=400)
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
    try:
        pdf_file = request.FILES.get('file')
        pages_str = request.POST.get('pages')

        reader, total_pages, error = validate_pdf_and_pages(pdf_file, pages_str)
        if error:
            return error

        pages_to_remove = parse_page_ranges(pages_str, total_pages)

        if not pages_to_remove:
            return JsonResponse({'error': 'No valid pages to remove.'}, status=400)
        if len(pages_to_remove) >= total_pages:
            return JsonResponse({'error': 'Cannot remove all pages from the PDF.'}, status=400)

        writer = PdfWriter()
        for i in range(total_pages):
            if i not in pages_to_remove:
                writer.add_page(reader.pages[i])

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_out:
            writer.write(temp_out)
            temp_out_path = temp_out.name

        if request.user.is_authenticated:
            save_operation(request, temp_out_path, OperationType.REMOVE_PAGES, [pdf_file.name])
        else:
            save_operation_temp(temp_out_path, OperationType.REMOVE_PAGES, [pdf_file.name])

        return FileResponse(open(temp_out_path, 'rb'), as_attachment=True)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
