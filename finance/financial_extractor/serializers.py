from rest_framework import serializers
from .models import Transcript, FinancialData

class TranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = ['id', 'file', 'uploaded_at']

    def validate(self, value):
        uploaded_file = value['file']
        # If file is greater than 10 MB, or less than 1 KB raise an error
        if uploaded_file.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size must be less than 10 MB")
        if uploaded_file.size < 1024:
            raise serializers.ValidationError("File size must be greater than 1 KB")
        return super().validate(value)

class FinancialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialData
        fields = ['id', 'transcript', 'category', 'fact_text', 'created_at']
