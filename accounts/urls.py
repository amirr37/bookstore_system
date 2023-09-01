from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.UserRegistrationAPIView.as_view(), name='register'),
    # path('login', views.LoginView.as_view(), name='login'),
    # path('logout', views.LogoutView.as_view(), name='logout'),
    # path('signup', views.SignupView.as_view(), name='signup'),
    path('profile', views.UserProfileAPIView.as_view(), name='profile'),
    # path('logintest', views.OTPView.as_view(), name='logintest')
    path('otp-login/', views.OTPLoginView.as_view(), name='otp-login'),
    path('reset-token/<int:user_id>', views.TokenResetView.as_view(), name='reset-token')
]
