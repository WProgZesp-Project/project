from .forms import UploadForm
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
import uuid
import os

SESSION_KEY = 'uploaded_files'

# 1. Strona główna: formularz + lista plików


def merge_page(request):
    form = UploadForm()
    uploaded = request.session.get(SESSION_KEY, [])
    return render(request, 'merge.html', {'form': form, 'uploaded': uploaded})

# 2. Obsługa uploadu


def upload_files(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('files')
            stored = request.session.get(SESSION_KEY, [])
            for f in files:
                filename = f"{uuid.uuid4().hex}_{f.name}"
                path = os.path.join(settings.MEDIA_ROOT, filename)
                with open(path, 'wb+') as dest:
                    for chunk in f.chunks():
                        dest.write(chunk)
                stored.append({'name': f.name, 'path': filename})
            request.session[SESSION_KEY] = stored
    return redirect('merge_page')

# 3. Zmiana kolejności


def reorder(request, direction, index):
    files = request.session.get(SESSION_KEY, [])
    index = int(index)
    if 0 <= index < len(files):
        new_index = index - 1 if direction == 'up' else index + 1
        if 0 <= new_index < len(files):
            files[index], files[new_index] = files[new_index], files[index]
            request.session[SESSION_KEY] = files
    return redirect('merge_page')

# 4. Kasowanie pliku


def delete_file(request, index):
    files = request.session.get(SESSION_KEY, [])
    info = files.pop(int(index))
    request.session[SESSION_KEY] = files
    os.remove(os.path.join(settings.MEDIA_ROOT, info['path']))
    return redirect('merge_page')

# 5. Scalanie i pobieranie


def merge_files(request):
    files = request.session.get(SESSION_KEY, [])
    merged_text = ''
    for info in files:
        with open(os.path.join(settings.MEDIA_ROOT, info['path']), encoding='utf-8') as f:
            merged_text += f.read() + '\n'
    response = HttpResponse(merged_text, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="merged.txt"'
    return response
