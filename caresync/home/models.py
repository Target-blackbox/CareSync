from django.db import models
from django.contrib.auth.hashers import make_password

class Patient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=255)  # Store hashed password
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
