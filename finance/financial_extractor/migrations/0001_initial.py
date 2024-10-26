# Generated by Django 4.2.16 on 2024-10-26 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transcript',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='transcripts/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FinancialData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Assets', 'Assets'), ('Expenditures', 'Expenditures'), ('Income', 'Income')], max_length=20)),
                ('fact_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('transcript', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='financial_data', to='financial_extractor.transcript')),
            ],
        ),
    ]
