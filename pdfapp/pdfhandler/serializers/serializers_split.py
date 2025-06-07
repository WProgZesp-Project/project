from rest_framework import serializers


class SplitPDFSerializer(serializers.Serializer):
    file = serializers.FileField()
    ranges = serializers.CharField(
        help_text='Enter page ranges, e.g., 1-3,5,7-9')
