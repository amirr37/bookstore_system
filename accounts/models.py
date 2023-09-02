import datetime
import random
import string
import uuid
from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

from accounts.sender import send_otp


# Create your models here.


#
class CustomUser(AbstractUser):
    MEMBERSHIP_CHOICES = [
        ('Free', 'Free'),
        ('Premium', 'Premium'),
    ]

    membership_type = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES, verbose_name='Membership Type',
                                       null=True)
    membership_expiry_date = models.DateField(verbose_name='Membership Expiry Date', null=True)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.get_full_name()


def generate_otp():
    return ''.join(random.SystemRandom().choice(string.digits) for _ in range(6))


class OTPRequest(models.Model):
    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # id of request
    phone_number = PhoneNumberField(null=True)
    otp_code = models.CharField(max_length=6, default=generate_otp)
    expire_time = models.DateTimeField(default=timezone.now() + timedelta(minutes=5))


class UserPayment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ], default='pending')
    description = models.TextField(blank=True)

    # Add more fields as needed

    def __str__(self):
        return f"{self.user.username}'s Payment - {self.payment_date}"
