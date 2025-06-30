import io
import zipfile

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.views.generic import TemplateView
from PyPDF2 import PdfReader, PdfWriter
from ..serializers.serializers_split import SplitPDFSerializer
from ..views.operation_history import save_operation, OperationType
from ..storages import DownloadableS3Storage


class SplitPDFTemplateView(TemplateView):
    template_name = "split_pdf.html"


class SplitPDFView(APIView):
    parser_classes = [MultiPartParser]

    def parse_ranges(self, ranges_str, total_pages):
        ranges = []
        for part in ranges_str.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
            else:
                start = end = int(part)
            start = max(1, start)
            end = min(total_pages, end)
            if start <= end:
                ranges.append((start, end))
        return ranges

    def validate_and_parse(self, request):
        serializer = SplitPDFSerializer(data=request.data)
        if not serializer.is_valid():
            return None, Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        pdf_file = serializer.validated_data['file']
        ranges_str = serializer.validated_data['ranges']
        reader = PdfReader(pdf_file)
        total_pages = len(reader.pages)
        page_ranges = self.parse_ranges(ranges_str, total_pages)
        if not page_ranges:
            return None, Response({"error": "Please provide at least one valid range."}, status=status.HTTP_400_BAD_REQUEST)
        return (pdf_file, reader, page_ranges, total_pages), None

    def save_to_s3(self, filename, output_stream):
        output_stream.seek(0)
        content_file = ContentFile(output_stream.read())
        s3_path = f"_temp/{filename}"
        content_file.name = s3_path
        storage = DownloadableS3Storage()
        storage.save(s3_path, content_file)
        return storage.url(s3_path), content_file

    def create_split_pdfs(self, reader, page_ranges):
        included_pages = set()
        download_links = []
        generated_files = []

        for start, end in page_ranges:
            writer = PdfWriter()
            for page_num in range(start - 1, end):
                writer.add_page(reader.pages[page_num])
                included_pages.add(page_num)

            output_stream = io.BytesIO()
            writer.write(output_stream)
            filename = f"split_{start}_{end}.pdf"
            file_url, file_obj = self.save_to_s3(filename, output_stream)

            download_links.append(
                f'<div class="download-btn"><a href="{file_url}" download class="btn">Download {filename}</a></div>'
            )
            generated_files.append((filename, file_obj.read()))

        return included_pages, download_links, generated_files

    def create_rest_pdf(self, reader, total_pages, included_pages):
        rest_writer = PdfWriter()
        for i in range(total_pages):
            if i not in included_pages:
                rest_writer.add_page(reader.pages[i])

        if rest_writer.pages:
            output_stream = io.BytesIO()
            rest_writer.write(output_stream)
            filename = "split_rest.pdf"
            file_url, file_obj = self.save_to_s3(filename, output_stream)
            download_link = (
                f'<div class="download-btn"><a href="{file_url}" download class="btn">Download {filename}</a></div>'
            )
            return download_link, (filename, file_obj.read())
        return None, None

    def create_and_save_zip(self, request, generated_files, original_filename):
        zip_stream = io.BytesIO()
        with zipfile.ZipFile(zip_stream, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for fname, fdata in generated_files:
                zipf.writestr(fname, fdata)
        zip_stream.seek(0)
        content_file = ContentFile(zip_stream.read())
        content_file.name = "split_result.zip"
        save_operation(
            request,
            content_file,
            OperationType.SPLIT,
            [original_filename]
        )

    def post(self, request):
        parsed_data, error_response = self.validate_and_parse(request)
        if error_response:
            return error_response
        pdf_file, reader, page_ranges, total_pages = parsed_data

        included_pages, download_links, generated_files = self.create_split_pdfs(reader, page_ranges)
        rest_download_link, rest_file = self.create_rest_pdf(reader, total_pages, included_pages)

        if rest_download_link:
            download_links.append(rest_download_link)
            generated_files.append(rest_file)

        if request.user.is_authenticated:
            self.create_and_save_zip(request, generated_files, pdf_file.name)

        return HttpResponse(
            "<p style='font-weight:bold;'>Your PDF has been split successfully!</p>"
            + "<br>".join(download_links)
        )
