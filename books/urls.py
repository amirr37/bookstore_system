from django.urls import path
from books import views

urlpatterns = [
    path('', views.BookListAPIView.as_view(), name='list-book'),
    path('create/', views.BookCreateAPIView.as_view(), name='create-book'),
    path('delete/<int:pk>', views.BookDeleteAPIView.as_view(), name='delete-book'),
    path('update/<int:pk>', views.BookUpdateAPIView.as_view(), name='update-book'),

]
