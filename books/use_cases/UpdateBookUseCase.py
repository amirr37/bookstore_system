from books.repositories import BookRepository


class UpdateBookUseCase:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def execute(self, book_id, book_data):
        return self.book_repository.update(book_id, book_data)
