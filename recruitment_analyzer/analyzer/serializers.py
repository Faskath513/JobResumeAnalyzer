from rest_framework import serializers
from .models import JobApplication


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['id', 'name', 'email', 'phone_number', 'job_position', 'resume', 'cover_letter', 'status',
                  'date_applied']
        read_only_fields = ['id', 'date_applied']

    def validate_email(self, value):
        """
        Check that the email address is unique when creating a new application.
        """
        if self.instance is None:  # Only validate on create
            if JobApplication.objects.filter(email=value).exists():
                raise serializers.ValidationError("An application with this email already exists.")
        return value

    def validate_status(self, value):
        """
        Ensure that the provided status is a valid choice.
        """
        valid_statuses = dict(self.Meta.model.STATUS_CHOICES)
        if value not in valid_statuses:
            raise serializers.ValidationError("Invalid status.")
        return value

    def validate(self, attrs):
        """
        Additional validation for the serializer.
        """
        # Validate status only if updating an existing instance
        if self.instance is not None and 'status' in attrs:
            self.validate_status(attrs['status'])

        # Add more complex validations here if necessary

        return attrs
