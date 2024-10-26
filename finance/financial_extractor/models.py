from django.db import models

# Create your models here.
from django.db import models

class Transcript(models.Model):
    file = models.FileField(upload_to='transcripts/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transcript {self.id} - {self.file.name}"

class FinancialData(models.Model):
    CATEGORY_CHOICES = [
        ('Assets', 'Assets'),
        ('Expenditures', 'Expenditures'),
        ('Income', 'Income'),
    ]

    transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE, related_name='financial_data')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    fact_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category}: {self.fact_text[:50]}"
