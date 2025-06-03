from django.db import models
from django.utils import timezone
from django.db.models import JSONField

class OperationType(models.TextChoices):
    MERGE = 'merge', 'Merge'
    SPLIT = 'split', 'Split'

class OperationHistory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=50, choices=OperationType.choices)
    created_at = models.DateTimeField(default=timezone.now)
    input_filenames = models.JSONField() # List of input filenames separated by commas
    result_filename = models.CharField(max_length=255)

    def __str__(self):
        return f"Merged: {self.input_filenames} at {self.created_at}"

