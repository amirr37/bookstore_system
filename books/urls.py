from django.urls import path
from books import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='book-list'),
    path('/<slug:slug>', views.BookDetailView.as_view(), name='book-detail'),
]
