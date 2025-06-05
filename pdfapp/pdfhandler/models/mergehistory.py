from django.db import models


class MergeHistory(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    filenames = models.TextField()
    merged_filename = models.CharField(max_length=255)
