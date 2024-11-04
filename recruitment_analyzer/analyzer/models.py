# analyzer/models.py
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from sympy.printing.codeprinter import requires


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Reviewed', 'Reviewed'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Rejected', 'Rejected'),
        ('Hired', 'Hired'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    job_position = models.CharField(max_length=100, help_text="Position applied for")
    resume = models.FileField(upload_to='resume/', help_text="Resume file" , blank=True, null=True )
    cover_letter = models.FileField(upload_to='cover/', help_text="Cover letter", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    date_applied = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_applied']
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"

    def __str__(self):
        return f"{self.name} - {self.job_position}"

    def is_recent_application(self):
        """Check if the application was submitted within the last 7 days."""
        return (timezone.now() - self.date_applied).days <= 7

    def clean(self):
        """Custom validation to ensure required fields are not empty and validate file types."""
        if not self.resume:
            raise ValidationError("A resume file is required.")
        if not self.cover_letter:
            raise ValidationError("A cover letter file is required.")

        if self.resume:
            if not self.resume.name.endswith('.pdf'):
                raise ValidationError("Resume must be a PDF file.")
            if self.resume.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError("Resume file size must be less than 2MB.")

        if self.cover_letter:
            if not self.cover_letter.name.endswith('.pdf'):
                raise ValidationError("Cover letter must be a PDF file.")
            if self.cover_letter.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError("Cover letter file size must be less than 2MB.")

    def save(self, *args, **kwargs):
        """Override save to enforce clean validation."""
        self.full_clean()  # This will call the clean() method
        super().save(*args, **kwargs)