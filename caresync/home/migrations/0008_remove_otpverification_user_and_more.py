# Generated by Django 5.0.6 on 2025-03-23 07:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0007_folderaccessrequest_otpverification"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="otpverification",
            name="user",
        ),
        migrations.DeleteModel(
            name="FolderAccessRequest",
        ),
        migrations.DeleteModel(
            name="OTPVerification",
        ),
    ]
