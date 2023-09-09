from books.repositories import BookRepository


class CreateBookUseCase:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def execute(self, book_data):
        return self.book_repository.create(book_data)
