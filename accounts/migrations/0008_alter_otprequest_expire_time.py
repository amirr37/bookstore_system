# Generated by Django 3.2.12 on 2023-08-31 14:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_otprequest_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otprequest',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 31, 14, 37, 18, 591476, tzinfo=utc)),
        ),
    ]
