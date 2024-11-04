# analyzer/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .resume_analysis import analyze_job_and_resume  # Make sure this import is correct
from .views import JobApplicationViewSet

app_name = 'analyzer'

# Create a router and register the JobApplicationViewSet
router = DefaultRouter()
router.register(r'applications', JobApplicationViewSet, basename='jobapplication')

urlpatterns = [
    path('', views.index, name='index'),
    path('applications/create/', views.create_job_application, name='create_job_application'),
    path('applications/view/', views.view_applications, name='view_applications'),
    path('applications/edit/<int:application_id>/', views.edit_job_application, name='edit_application'),
    path('applications/delete/<int:application_id>/', views.delete_job_application, name='delete_application'),
    path('api/', include(router.urls)),  # Include the router URLs for the API
    path('analyze/', analyze_job_and_resume, name='analyze_job_and_resume'),  # URL for analyze

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
