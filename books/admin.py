from django.contrib import admin

from books.models import Book, Genre


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'genre', 'publication_date', 'isbn', 'price')
    list_filter = ('genre', 'publication_date')
    search_fields = ('title', 'authors', 'isbn')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('title',)
