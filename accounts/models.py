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
    phone_number = PhoneNumberField(blank=True, null=True,  unique=True)

    def __str__(self):
        return self.get_full_name()


def generate_otp():
    return ''.join(random.SystemRandom().choice(string.digits) for _ in range(6))


class OTPRequest(models.Model):
    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # id of request
    phone_number = PhoneNumberField(null=True)
    otp_code = models.CharField(max_length=6, default=generate_otp)
    expire_time = models.DateTimeField(default=timezone.now() + timedelta(minutes=5))
