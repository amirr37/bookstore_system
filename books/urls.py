from django.urls import path
from books import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='list-book'),
    path('create/', views.BookCreateView.as_view(), name='create-book'),
    path('delete/<int:pk>', views.BookDeleteView.as_view(), name='delete-book'),
    path('update/<int:pk>', views.BookUpdateView.as_view(), name='update-book'),

]
