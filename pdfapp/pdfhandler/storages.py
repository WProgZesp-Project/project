from storages.backends.s3boto3 import S3Boto3Storage
import os

class DownloadableS3Storage(S3Boto3Storage):
    def get_object_parameters(self, name):
        path_parts = name.split('/')
        if len(path_parts) >= 2:
            operation, filename = path_parts[1], path_parts[-1]
            new_download_name = f"{operation}_{filename}"
        else:
            new_download_name = os.path.basename(name)

        return {
            'ContentDisposition': f'attachment; filename="{new_download_name}"'
        }