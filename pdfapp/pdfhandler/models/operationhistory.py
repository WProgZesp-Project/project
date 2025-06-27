from django.db import models
from django.utils import timezone


class OperationType(models.TextChoices):
    MERGE = 'merge', 'Merge'
    SPLIT = 'split', 'Split'
    EXTRACT = 'extract', "Extract"
    REMOVE_PAGES = 'remove_pages', "Remove Pages"
    REMOVE_PASSWORD = "remove_password", "Remove Password"
    COMPRESS_AND_ZIP = "compress_and_zip", "Compress to ZIP"


class OperationHistory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=50, choices=OperationType.choices)
    created_at = models.DateTimeField(default=timezone.now)
    input_filenames = models.JSONField()  # List of input filenames separated by commas
    result_filename = models.CharField(max_length=255)

    def __str__(self):
        return f"Merged: {self.input_filenames} at {self.created_at}"
