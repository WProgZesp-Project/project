from rest_framework import serializers
from ..models import OperationHistory


class OperationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationHistory
        fields = ['id', 'user', 'operation_type', 'created_at', 'input_filenames', 'result_file']
        read_only_fields = ['id', 'created_at', 'user']
