# Generated by Django 5.0.3 on 2024-05-13 12:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("electrode", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="electrodecategory",
            name="label",
        ),
    ]