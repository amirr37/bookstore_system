from books.repositories import BookRepository


class DeleteBookUseCase:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def execute(self, book_id):
        return self.book_repository.delete(book_id)
