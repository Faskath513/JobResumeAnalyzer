# analyzer/services.py

from django.utils import timezone
from datetime import timedelta
from .models import JobApplication
from django.core.mail import send_mail
from django.conf import settings

def get_recent_applications(days=7):
    """
    Retrieve job applications submitted within the last `days` days.
    """
    recent_date = timezone.now() - timedelta(days=days)
    return JobApplication.objects.filter(date_applied__gte=recent_date)

def update_application_status(application_id, new_status):
    """
    Update the status of a job application and return the updated instance.
    """
    try:
        application = JobApplication.objects.get(id=application_id)
        if new_status in dict(JobApplication.STATUS_CHOICES):
            application.status = new_status
            application.save()
            return application
        else:
            raise ValueError("Invalid status value")
    except JobApplication.DoesNotExist:
        return None

def send_status_update_email(application):
    subject = f"Your application status for {application.job_position} has been updated"
    message = f"Dear {application.name},\n\nYour application status has been updated to: {application.status}.\n\nThank you for applying!"
    recipient = application.email

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
        fail_silently=False,
    )
    return f"Status update email sent to {recipient}"
