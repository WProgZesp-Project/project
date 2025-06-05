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

            if not page_ranges or len(page_ranges) > 1:
                return Response(
                    {"error": "Please provide exactly one range, e.g., '1-3'."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            start, end = page_ranges[0]
            writer = PdfWriter()
            for page_num in range(start - 1, end):
                writer.add_page(reader.pages[page_num])

            output_stream = io.BytesIO()
            writer.write(output_stream)
            output_stream.seek(0)

            filename = f"split_{start}_{end}.pdf"
            save_path = os.path.join(settings.MEDIA_ROOT, filename)

            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(output_stream.read())

            file_url = f"{settings.MEDIA_URL}{filename}"

            return HttpResponse(f'''
                <p style="font-weight:bold;">Your PDF has been split successfully!</p>
                <a href="{file_url}" download class="btn">Download Split PDF</a>
            ''')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
