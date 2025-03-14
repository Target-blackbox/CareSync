from django.db import models
from django.utils import timezone
from home.models import CustomUser

# Create your models here.

class ReportFolder(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='folders')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['name', 'user']  # Prevent duplicate folder names for the same user

    def __str__(self):
        return f"{self.user.username}'s {self.name} folder"

class Report(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='reports/')
    folder = models.ForeignKey(ReportFolder, on_delete=models.CASCADE, related_name='reports')
    uploaded_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reports')

    def __str__(self):
        return self.title
