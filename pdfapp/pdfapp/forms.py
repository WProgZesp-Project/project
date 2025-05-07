from django import forms
from django.forms.widgets import ClearableFileInput


class MultiFileInput(ClearableFileInput):
    allow_multiple_selected = True


class UploadForm(forms.Form):
    files = forms.FileField(
        widget=MultiFileInput,
        label='Wybierz pliki',
        help_text='Możesz wybrać wiele plików'
    )
