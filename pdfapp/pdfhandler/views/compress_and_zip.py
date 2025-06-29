from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from ..views.operation_history import save_operation, OperationType
from ..storages import DownloadableS3Storage

import io
import zipfile
from django.core.files.base import ContentFile


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
        unique_filename = f"compress_{filenames[0][:-4]}.zip"

        if request.user.is_authenticated:
            content_file = ContentFile(zip_data)
            content_file.name = unique_filename
            save_operation(request, content_file, OperationType.COMPRESS_AND_ZIP, filenames)

            # Response for immediate download (even if saved in OperationHistory)
            response = HttpResponse(zip_data, content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{unique_filename}"'
            return response

        # Dla anonimowego użytkownika — zapis do S3 _temp
        content_file = ContentFile(zip_data)
        s3_key = f"_temp/{unique_filename}"
        content_file.name = s3_key

        storage = DownloadableS3Storage()
        storage.save(s3_key, content_file)

        s3_url = storage.url(s3_key)
        html = f'''
            <p style="font-weight:bold;">ZIP file created successfully!</p>
            <div class="download-btn">
                <a href="{s3_url}" class="btn" download>Download ZIP</a>
            </div>
        '''
        return HttpResponse(html)

    return render(request, 'compress_zip.html')
