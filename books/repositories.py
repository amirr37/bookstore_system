from books.models import Book
from abc import ABC, abstractmethod


class BookRepository(ABC):
    @abstractmethod
    def create(self, book_data):
        pass

    @abstractmethod
    def update(self, book_id, book_data):
        pass

    @abstractmethod
    def delete(self, book_id):
        pass

    @abstractmethod
    def get_by_id(self, book_id):
        pass

    @abstractmethod
    def get_all(self):
        pass


class DjangoBookRepository(BookRepository):
    def create(self, book_data):
        return Book.objects.create(**book_data)

    def update(self, book_id, book_data):
        book = self.get_by_id(book_id)
        for key, value in book_data.items():
            setattr(book, key, value)
        book.save()
        return book

    def delete(self, book_id):
        book = self.get_by_id(book_id)
        book.delete()

    def get_by_id(self, book_id):
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None

    def get_all(self, filters=None):
        queryset = Book.objects.all()
        if filters:
            queryset = queryset.filter(**filters)

        return queryset
