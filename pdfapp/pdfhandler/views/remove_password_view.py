from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
from PyPDF2 import PdfReader, PdfWriter
import tempfile

@csrf_exempt
@require_POST
def remove_pdf_password(request):
    pdf_file = request.FILES.get('file')
    password = request.POST.get('password')
    if not pdf_file or not password:
        return JsonResponse({'error': 'File and password are required.'}, status=400)
    try:
        reader = PdfReader(pdf_file)
        if reader.is_encrypted:
            if not reader.decrypt(password):
                return JsonResponse({'error': 'Incorrect password.'}, status=400)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_out:
            writer.write(temp_out)
            temp_out_path = temp_out.name
        response = FileResponse(open(temp_out_path, 'rb'), as_attachment=True, filename='unlocked.pdf')
        return response
    except Exception as e:
        return JsonResponse({'error': f'Failed to process PDF: {str(e)}'}, status=400)

def remove_password_page(request):
    return render(request, 'remove_password.html')
