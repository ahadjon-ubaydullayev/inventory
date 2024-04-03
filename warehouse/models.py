from django.db import models
from django.contrib.auth.models import AbstractUser


class Mahsulot(models.Model):
    nomi = models.CharField(max_length=255)
    kategoriya = models.CharField(max_length=255, blank=True, null=True)
    qadoq = models.IntegerField(default=0, blank=True, null=True)  # pachka
    quti = models.IntegerField(default=0)  # karobka
    massa = models.IntegerField(default=0)
    miqdori = models.IntegerField(default=0)
    kelgan_sana = models.DateField(auto_now_add=True)
    tavsifi = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nomi


class CustomUser(AbstractUser):
    is_manager = models.BooleanField(default=False)

    # Define unique related_names for groups and user_permissions fields
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        related_name='customuser_set',  # Provide a unique related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        related_name='customuser_set',  # Provide a unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
    )
