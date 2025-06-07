import io
import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from django.conf import settings
from PyPDF2 import PdfReader, PdfWriter
from ..serializers.serializers_split import SplitPDFSerializer


class SplitPDFTemplateView(TemplateView):
    template_name = "split_pdf.html"


class SplitPDFView(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request):
        return render(request, 'pdfhandler/split_pdf.html')

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

    def post(self, request):
        serializer = SplitPDFSerializer(data=request.data)
        if serializer.is_valid():
            pdf_file = serializer.validated_data['file']
            ranges_str = serializer.validated_data['ranges']

            reader = PdfReader(pdf_file)
            total_pages = len(reader.pages)
            page_ranges = self.parse_ranges(ranges_str, total_pages)

            if not page_ranges:
                return Response(
                    {"error": "Please provide at least one valid range."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Track which pages have been included
            included_pages = set()
            download_links = []

            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

            for start, end in page_ranges:
                writer = PdfWriter()
                for page_num in range(start - 1, end):
                    writer.add_page(reader.pages[page_num])
                    included_pages.add(page_num)

                output_stream = io.BytesIO()
                writer.write(output_stream)
                output_stream.seek(0)

                filename = f"split_{start}_{end}.pdf"
                save_path = os.path.join(settings.MEDIA_ROOT, filename)

                with open(save_path, 'wb') as f:
                    f.write(output_stream.read())

                file_url = f"{settings.MEDIA_URL}{filename}"
                download_links.append(f'<div class="download-btn"><a href="{file_url}" download class="btn">Download {filename}</a></div>')


            # Handle the rest of the pages
            rest_writer = PdfWriter()
            for i in range(total_pages):
                if i not in included_pages:
                    rest_writer.add_page(reader.pages[i])

            if rest_writer.pages:
                output_stream = io.BytesIO()
                rest_writer.write(output_stream)
                output_stream.seek(0)

                rest_filename = "split_rest.pdf"
                save_path = os.path.join(settings.MEDIA_ROOT, rest_filename)
                with open(save_path, 'wb') as f:
                    f.write(output_stream.read())

                rest_file_url = f"{settings.MEDIA_URL}{rest_filename}"
                download_links.append(f'<div class="download-btn"><a href="{rest_file_url}" download class="btn">Download split_rest.pdf</a></div>')


            return HttpResponse('''
                <p style="font-weight:bold;">Your PDF has been split successfully!</p>
                {}
            '''.format('<br>'.join(download_links)))
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
