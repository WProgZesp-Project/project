from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from PyPDF2 import PdfReader, PdfWriter
from django.shortcuts import render
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

@csrf_exempt
@require_POST
def remove_pdf_pages(request):
    pdf_file = request.FILES.get('file')
    pages_str = request.POST.get('pages')

    if not pdf_file or not pages_str:
        return JsonResponse(
            {'error': 'PDF file and pages to remove are required.'}, status=400)

    try:
        reader = PdfReader(pdf_file)
        total_pages = len(reader.pages)
    except Exception:
        return JsonResponse({'error': 'Failed to read PDF file.'}, status=400)

    try:
        raw_pages_to_remove = parse_page_ranges(pages_str)

        pages_to_remove = set()
        for p in raw_pages_to_remove:
            if not isinstance(p, int) or p < 0 or p >= total_pages:
                return JsonResponse({
                    'error': f'Page number {p + 1} is out of range. PDF has {total_pages} pages.'
                }, status=400)
            pages_to_remove.add(p)

        if len(pages_to_remove) >= total_pages:
            return JsonResponse({
                'error': 'Cannot remove all pages from the PDF file.'
            }, status=400)

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

        return FileResponse(
            open(temp_out_path, 'rb'),
            as_attachment=True,
            filename=f'{os.path.splitext(pdf_file.name)[0]} (removed-pages).pdf'
        )

    except ValueError:
        return JsonResponse({
            'error': 'Invalid pages format. Use format like 1,2,4-6.'
        }, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
