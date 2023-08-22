from django.contrib import admin
from accounts.models import OTPRequest


# Register your models here.


@admin.register(OTPRequest)
class OTPRequestAdmin(admin.ModelAdmin):
    pass
