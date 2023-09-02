from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.UserRegistrationAPIView.as_view(), name='register'),

    path('user/profile/', views.UserProfileAPIView.as_view(), name='profile'),


    path('otp/login/', views.OTPSMSService1.as_view(), name='otp-login'),
    path('otp/verify/', views.OTPVerifyView.as_view(), name='otp-verify'),

    path('reset-token/<int:user_id>', views.TokenResetView.as_view(), name='reset-token')


]
