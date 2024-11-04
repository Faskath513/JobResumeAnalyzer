
# analyzer/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import JobApplication

class JobApplicationTests(APITestCase):
    def setUp(self):
        self.job_application_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone_number': '1234567890',
            'job_position': 'Software Engineer',
            'resume': 'This is a sample resume text.',
            'cover_letter': 'This is a sample cover letter.'
        }
        self.application = JobApplication.objects.create(**self.job_application_data)

    def test_create_job_application(self):
        """
        Ensure we can create a new job application.
        """
        url = reverse('jobapplication-list')
        response = self.client.post(url, self.job_application_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JobApplication.objects.count(), 2)  # One from setup, one created here
        self.assertEqual(response.data['name'], self.job_application_data['name'])

    def test_list_job_applications(self):
        """
        Ensure we can list all job applications.
        """
        url = reverse('jobapplication-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_job_application(self):
        """
        Ensure we can retrieve a single job application.
        """
        url = reverse('jobapplication-detail', args=[self.application.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.application.name)

    def test_update_job_application(self):
        """
        Ensure we can update a job application.
        """
        url = reverse('jobapplication-detail', args=[self.application.id])
        updated_data = {
            'name': 'Jane Doe',
            'email': 'jane.doe@example.com',
            'job_position': 'Data Scientist'
        }
        response = self.client.put(url, {**self.job_application_data, **updated_data}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.application.refresh_from_db()
        self.assertEqual(self.application.name, 'Jane Doe')
        self.assertEqual(self.application.email, 'jane.doe@example.com')

    def test_delete_job_application(self):
        """
        Ensure we can delete a job application.
        """
        url = reverse('jobapplication-detail', args=[self.application.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(JobApplication.objects.count(), 0)

    def test_recent_job_applications(self):
        """
        Ensure we can get job applications from the last 7 days using the recent endpoint.
        """
        url = reverse('jobapplication-recent')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_status(self):
        """
        Ensure we can update the status of a job application.
        """
        url = reverse('jobapplication-update-status', args=[self.application.id])
        response = self.client.post(url, {'status': 'Reviewed'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.application.refresh_from_db()
        self.assertEqual(self.application.status, 'Reviewed')

    def test_update_status_invalid(self):
        """
        Ensure an invalid status update returns a 400 response.
        """
        url = reverse('jobapplication-update-status', args=[self.application.id])
        response = self.client.post(url, {'status': 'Unknown Status'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
