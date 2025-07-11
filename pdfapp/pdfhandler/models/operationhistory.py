from django.db import models
from django.utils import timezone


class OperationType(models.TextChoices):
    MERGE = 'merge', 'Merge'
    SPLIT = 'split', 'Split'
    EXTRACT = 'extract', "Extract"
    REMOVE_PAGES = 'remove_pages', "Remove Pages"
    REMOVE_PASSWORD = "remove_password", "Remove Password"
    ADD_PASSWORD = "add_password", "Add Password"
    COMPRESS_AND_ZIP = "compress", "Compress to ZIP"


def user_operation_path(instance, filename):
    return f"{instance.user.username}/{instance.operation_type}/{filename}"


class OperationHistory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=50, choices=OperationType.choices)
    created_at = models.DateTimeField(default=timezone.now)
    input_filenames = models.JSONField()  # list[str]
    result_file = models.FileField(upload_to=user_operation_path)

    def __str__(self):
        return f"{self.operation_type.capitalize()}: {self.input_filenames} at {self.created_at}"
