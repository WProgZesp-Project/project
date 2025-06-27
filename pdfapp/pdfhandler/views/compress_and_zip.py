from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from ..models import OperationHistory, OperationType
import io
import os
import zipfile
from datetime import datetime


@csrf_exempt
def compress_and_zip(request):
    if request.method == 'POST':
        zip_buffer = io.BytesIO()
        filenames = []
        with zipfile.ZipFile(zip_buffer, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
            for f in request.FILES.getlist('pdf_files'):
                filenames.append(f.name)
                zip_file.writestr(f.name, f.read())

        zip_buffer.seek(0)
        zip_data = zip_buffer.read()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"compressed_{timestamp}.zip"
        if request.user.is_authenticated:
            OperationHistory.objects.create(
                user=request.user,
                operation_type=OperationType.COMPRESS_AND_ZIP,
                input_filenames=filenames,
                result_filename=unique_filename
            )

            media_path = os.path.join(settings.MEDIA_ROOT, unique_filename)
            with open(media_path, "wb") as f:
                f.write(zip_data)

        response = HttpResponse(zip_data, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{unique_filename}"'
        return response

    return render(request, 'compress_zip.html')
