from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    # path('signup', views.SignupView.as_view(), name='signup'),
    path('profile', views.UserProfileView.as_view(), name='profile'),
    path('logintest', views.OTPView.as_view(), name='logintest')
]
