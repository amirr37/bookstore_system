# Generated by Django 3.2.12 on 2023-08-31 13:54

import accounts.models
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_customuser_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otprequest',
            name='created',
        ),
        migrations.RemoveField(
            model_name='otprequest',
            name='password',
        ),
        migrations.RemoveField(
            model_name='otprequest',
            name='receiver',
        ),
        migrations.AddField(
            model_name='otprequest',
            name='otp_code',
            field=models.CharField(default=accounts.models.generate_otp, max_length=6),
        ),
        migrations.AddField(
            model_name='otprequest',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None),
        ),
    ]
