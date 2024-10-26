from rest_framework import serializers
from .models import Transcript, FinancialData

class TranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = ['id', 'file', 'uploaded_at']

class FinancialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialData
        fields = ['id', 'transcript', 'category', 'fact_text', 'created_at']
