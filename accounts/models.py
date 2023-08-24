import random
import string
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

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

    def __str__(self):
        return self.get_full_name()


def generate_otp():
    return ''.join(random.SystemRandom().choice(string.digits) for _ in range(4))


class OTPRequest(models.Model):
    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # id of request
    receiver = models.CharField(max_length=50)
    password = models.CharField(max_length=4, default=generate_otp)
    created = models.DateTimeField(auto_now_add=True, editable=False)
