from django.contrib import admin

from books.models import Book, Genre, Author, City


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'publication_date', 'isbn', 'price')
    list_filter = ('genre', 'publication_date')
    search_fields = ('title', 'authors', 'isbn')
    readonly_fields = ["slug"]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
