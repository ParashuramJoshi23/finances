from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transcript, FinancialData
from .serializers import TranscriptSerializer, FinancialDataSerializer
from django.conf import settings

class TranscriptUploadView(APIView):
    def post(self, request, format=None):
        # TODO: Implement authorization, on who can upload.
        serializer = TranscriptSerializer(data=request.data)
        if serializer.is_valid():
            transcript_instance : Transcript = serializer.save()
            from .utils import process_transcript 
            process_transcript(transcript_instance)
            return Response({'message': 'File processed successfully', 'transcript_id': transcript_instance.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FinancialDataListView(APIView):
    def get(self, request, transcript_id, format=None):
        # TODO: Implement check if financial data is being calculated.
        # TODO: Handle cases where data is not valid, or not found.
        financial_data = FinancialData.objects.filter(transcript_id=transcript_id)
        serializer = FinancialDataSerializer(financial_data, many=True)
        return Response(serializer.data)
