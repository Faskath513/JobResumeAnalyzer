import os

from django.conf import settings
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


from .forms import JobApplicationForm
from .models import JobApplication
from .serializers import JobApplicationSerializer
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .resume_analysis import analyze_job_and_resume


def analyze_resumes(resumes_folder, job_description):
    # Implement your logic to analyze resumes here
    results = []  # Replace with actual analysis results

    # Example of processing files in resumes_folder
    for resume_file in os.listdir(resumes_folder):
        file_path = os.path.join(resumes_folder, resume_file)
        # Dummy logic to add results, replace with actual analysis
        results.append({
            'filename': resume_file,
            'matched': 'Yes' if job_description in resume_file else 'No'  # Example matching logic
        })

    return results


def analyze_resumes_view(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('resumes')  # Get uploaded files
        job_description = request.POST.get('job_description')  # Get job description

        # Save uploaded files to a temporary folder
        resumes_folder = os.path.join(settings.MEDIA_ROOT, 'temp_resumes')  # Change to a suitable path
        os.makedirs(resumes_folder, exist_ok=True)

        # Save the uploaded resumes
        for uploaded_file in uploaded_files:
            fs = FileSystemStorage(resumes_folder)
            fs.save(uploaded_file.name, uploaded_file)

        # Analyze resumes
        results = analyze_resumes(resumes_folder, job_description)

        # Clean up the temporary folder after analysis
        for file_name in os.listdir(resumes_folder):
            file_path = os.path.join(resumes_folder, file_name)
            os.remove(file_path)
        os.rmdir(resumes_folder)  # Remove the folder after cleaning up

        # Render the results in the template
        return render(request, 'job_and_resume_analysis_result.html', {'results': results})

    return render(request, 'upload_job_and_resume.html')
def view_applications(request):
    """Handles displaying the list of job applications."""
    applications = JobApplication.objects.all()  # Fetch all applications
    return render(request, 'analyzer/view_applications_form.html', {'applications': applications})


def create_job_application(request):
    """Handles the creation of job applications."""
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application submitted successfully.')
            return redirect('analyzer:view_applications')  # Redirecting to applications view
        else:
            messages.error(request, 'Please correct the errors below.')  # Show general error message

    else:
        form = JobApplicationForm()

    return render(request, 'analyzer/job_application_form.html', {'form': form})


def edit_job_application(request, application_id):
    """Handles editing an existing job application."""
    application = get_object_or_404(JobApplication, id=application_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application updated successfully.')
            return redirect('analyzer:view_applications')
    else:
        form = JobApplicationForm(instance=application)

    return render(request, 'analyzer/job_application_form.html', {'form': form})


def delete_job_application(request, application_id):
    """Handles the deletion of a job application."""
    application = get_object_or_404(JobApplication, id=application_id)
    if request.method == 'POST':
        application.delete()
        messages.success(request, 'Application deleted successfully.')
        return redirect('analyzer:view_applications')

    return render(request, 'analyzer/confirm_delete.html', {'application': application})


def index(request):
    """Displays the index page with all job applications."""
    applications = JobApplication.objects.all()  # Get all applications
    return render(request, 'index.html', {'applications': applications})


class JobApplicationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing job application instances.
    """
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Returns applications submitted within the last X days (default 7).
        """
        days_ago = request.query_params.get('days', 7)
        try:
            days_ago = int(days_ago)
        except ValueError:
            return Response(
                {"error": "Invalid number of days provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        recent_date = timezone.now() - timedelta(days=days_ago)
        recent_applications = JobApplication.objects.filter(date_applied__gte=recent_date)

        serializer = self.get_serializer(recent_applications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """
        Updates the status of a specific job application.
        """
        job_application = self.get_object()
        new_status = request.data.get('status')

        # Check if the new status is valid
        valid_statuses = dict(JobApplication.STATUS_CHOICES)
        if new_status not in valid_statuses:
            return Response(
                {"error": "Invalid status provided. Choose from: {}".format(', '.join(valid_statuses.keys()))},
                status=status.HTTP_400_BAD_REQUEST
            )

        job_application.status = new_status
        job_application.save()
        serializer = self.get_serializer(job_application)
        return Response(serializer.data, status=status.HTTP_200_OK)
