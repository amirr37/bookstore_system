from django.shortcuts import render
from django.views.generic import ListView, DetailView

from books.models import Book


# Create your views here.


class BookListView(ListView):
    model = Book
    context_object_name = 'books'
    paginate_by = 5


# class BookDetailView(DetailView):
#     model = Book
#     template_name = 'book_detail.html'  # Replace with your actual template name
#     context_object_name = 'book'  # The name you'll use in the template to refer to the book object
#