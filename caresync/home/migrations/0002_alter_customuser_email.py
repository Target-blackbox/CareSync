# Generated by Django 5.0.6 on 2025-03-11 14:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
