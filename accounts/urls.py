from django.urls import path
from accounts import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('', views.IndexPageView.as_view(), name='index')
]
