# Generated by Django 5.1.2 on 2024-11-04 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('job_position', models.CharField(help_text='Position applied for', max_length=100)),
                ('resume', models.FileField(blank=True, help_text='Resume file', null=True, upload_to='resume/')),
                ('cover_letter', models.FileField(blank=True, help_text='Cover letter', null=True, upload_to='cover/')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Reviewed', 'Reviewed'), ('Interview Scheduled', 'Interview Scheduled'), ('Rejected', 'Rejected'), ('Hired', 'Hired')], default='Pending', max_length=20)),
                ('date_applied', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Job Application',
                'verbose_name_plural': 'Job Applications',
                'ordering': ['-date_applied'],
            },
        ),
    ]
