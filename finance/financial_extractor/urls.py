from django.urls import path
from .rest_api import TranscriptUploadView, FinancialDataListView

urlpatterns = [
    path('upload/', TranscriptUploadView.as_view(), name='transcript-upload'),
    path('financial-data/<int:transcript_id>/', FinancialDataListView.as_view(), name='financial-data-list'),
]
