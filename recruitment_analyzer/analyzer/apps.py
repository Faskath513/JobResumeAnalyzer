# analyzer/apps.py

from django.apps import AppConfig

class AnalyzerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analyzer'
    verbose_name = "Job Application Analyzer"
