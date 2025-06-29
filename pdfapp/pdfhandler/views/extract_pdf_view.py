from rest_framework import (
    generics,
    permissions,
)
from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from PyPDF2 import PdfReader, PdfWriter
from ..views.operation_history import save_operation, OperationType
import tempfile
import os


class ExtractPagesView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'Missing file.'}, status=400)
        pdf_file = request.FILES['file']

        pages_param = request.POST.get('pages', '')
        if not pages_param:
            return JsonResponse(
                {'error': 'Missing pages parameter.'}, status=400
            )

        try:
            page_numbers = self._parse_page_numbers(pages_param)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

        try:
            pdf_reader = PdfReader(pdf_file)
        except Exception as e:
            return JsonResponse(
                {'error': f'Error reading PDF file: {e}'}, status=400
            )

        pdf_writer = PdfWriter()
        for page_num in page_numbers:
            if 0 <= page_num - 1 < len(pdf_reader.pages):
                pdf_writer.add_page(pdf_reader.pages[page_num - 1])
            else:
                return JsonResponse(
                    {
                        'error': f'Page number {page_num} is out of range.'
                    },
                    status=400
                )

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp:
            pdf_writer.write(temp)
            temp_out_path = temp.name

        if request.user.is_authenticated:
            save_operation(request, temp_out_path, OperationType.EXTRACT, [pdf_file.name])

        response = FileResponse(
            open(temp_out_path, 'rb'),
            as_attachment=True
        )
        return response

    def get(self, request):
        return render(request, "extract.html")

    def _parse_page_numbers(self, pages_string):
        """
        Parses a comma-separated string of page numbers
        and ranges into a list of integers.

        Handles individual page numbers (e.g., "1") and ranges (e.g., "3-5").

        Args:
            pages_string:  The string to parse (e.g., "1,3,5-7,9").

        Returns:
            A list of integers representing the page numbers
            (e.g., [1, 3, 5, 6, 7, 9]).

        Raises:
            ValueError:  If the string is malformed.
        """
        page_numbers = []
        parts = pages_string.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                try:
                    start, end = map(int, part.split('-'))
                    if start > end:
                        raise ValueError(
                            (
                                "Range start must be less"
                                "than or equal to range end"
                            )
                        )
                    page_numbers.extend(range(start, end + 1))
                except ValueError:
                    raise ValueError(f"Invalid page range: {part}")
            else:
                try:
                    page_number = int(part)
                    if page_number < 1:
                        raise ValueError(
                            "Page numbers must be greater than zero"
                        )
                    page_numbers.append(page_number)
                except ValueError:
                    raise ValueError(f"Invalid page number: {part}")
        return page_numbers
