from django.urls import path
from books import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='book-list'),
    path('<slug:slug>', views.BookDetailView.as_view(), name='book-detail'),
    path('<slug:slug>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    path('books/create/', views.BookCreateView.as_view(), name='create-book'),

]
