from django.db import models
from django.contrib.auth.models import AbstractUser


class Mahsulot(models.Model):
    nomi = models.CharField(max_length=255)
    kategoriya = models.CharField(max_length=255, blank=True, null=True)
    qadoq = models.IntegerField(default=0, blank=True, null=True)  # pachka
    quti = models.IntegerField(default=0)  # karobka
    massa = models.FloatField(default=0)
    miqdori = models.IntegerField(default=0)
    kelgan_sana = models.DateField(auto_now_add=True)
    tavsifi = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nomi


class Customer(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    photo = models.ImageField(
        upload_to='profile_photos', null=True, blank=True)
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


# class ProductHistory(models.Model):
#     product_id = models.IntegerField()
#     transaction_type = models.CharField(
#         max_length=10)  # 'Addition' or 'Sending'
#     quantity = models.IntegerField()
#     customer_id = models.IntegerField(blank=True, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     description = models.TextField(blank=True, null=True)

class ProductHistory(models.Model):
    ACTION_CHOICES = [
        ('ADD', 'Added'),
        ('SEND', 'Sent to Customer'),
    ]

    # Assuming you have a Product model
    product = models.ForeignKey(
        'Mahsulot', on_delete=models.CASCADE, related_name='history')
    transaction_type = models.CharField(max_length=10, choices=ACTION_CHOICES)
    quantity = models.IntegerField()
    # Using ForeignKey to reference Customer
    customer = models.ForeignKey(
        'Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='history')
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.nomi} - {self.get_transaction_type_display()}"
