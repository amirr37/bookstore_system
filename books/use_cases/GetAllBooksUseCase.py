from books.repositories import DjangoBookRepository


class GetAllBooksUseCase:
    def __init__(self, book_repository: DjangoBookRepository):
        self.book_repository = book_repository

    def execute(self, filters=None):
        return self.book_repository.get_all(filters)
