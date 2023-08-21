from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, TemplateView
from rest_framework import generics
from accounts.serializers import UserRegistrationSerializer

from books.forms import BookForm
from books.models import Book


# Create your views here.



class BookListView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = 'books'
    paginate_by = 5


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'  # Replace with your actual template name
    context_object_name = 'book'  # The name you'll use in the template to refer to the book object


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'books/book_delete.html'  # Create this template
    success_url = reverse_lazy('book_list')  # Redirect after successful deletion


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_create.html'
    success_url = reverse_lazy('book-list')

# -----------------------------------------------------------------
