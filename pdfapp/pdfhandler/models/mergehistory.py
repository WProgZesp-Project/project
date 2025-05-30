from django.db import models
from django.utils import timezone


class MergeHistory(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    filenames = models.TextField()  # Comma-separated list of filenames
    merged_filename = models.CharField(max_length=255)

    def __str__(self):
        return f"Merged: {self.filenames} at {self.timestamp}"
