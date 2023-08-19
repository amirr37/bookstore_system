from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


#
class CustomUser(AbstractUser):
    MEMBERSHIP_CHOICES = [
        ('Free', 'Free'),
        ('Premium', 'Premium'),
    ]

    membership_type = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES, verbose_name='Membership Type')
    membership_expiry_date = models.DateField(verbose_name='Membership Expiry Date')

    def __str__(self):
        return self.get_full_name()
