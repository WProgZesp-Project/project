# Generated by Django 5.2.3 on 2025-06-28 23:50

import pdfhandler.models.operationhistory
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdfhandler', '0003_remove_operationhistory_result_filename_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationhistory',
            name='result_file',
            field=models.FileField(upload_to=pdfhandler.models.operationhistory.user_operation_path),
        ),
    ]
