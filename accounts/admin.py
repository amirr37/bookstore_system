from django.contrib import admin
from accounts.models import OTPRequest, CustomUser


# Register your models here.


@admin.register(OTPRequest)
class OTPRequestAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

