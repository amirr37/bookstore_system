from django.http import Http404
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Book
from .serializers import BookSerializer
from .filters import BookFilter
# Import your use cases and repositories
from books.use_cases.CreateBookUseCase import CreateBookUseCase
from .use_cases.UpdateBookUseCase import UpdateBookUseCase
from .use_cases.DeleteBookUseCase import DeleteBookUseCase
from .use_cases.GetBookByIDUseCase import GetBookByIDUseCase
from .use_cases.GetAllBooksUseCase import GetAllBooksUseCase
from .repositories import DjangoBookRepository

# Create instances of repository classes
book_repository = DjangoBookRepository()

# Create instances of use cases with injected repositories
create_book_use_case = CreateBookUseCase(book_repository)
update_book_use_case = UpdateBookUseCase(book_repository)
delete_book_use_case = DeleteBookUseCase(book_repository)
get_book_by_id_use_case = GetBookByIDUseCase(book_repository)
get_all_books_use_case = GetAllBooksUseCase(book_repository)


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter  # Assign the filterset class
    pagination_class = PageNumberPagination  # Set the pagination class
    pagination_class.page_size = 10

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())  # Apply filters
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookDeleteAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class BookUpdateAPIView(APIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def put(self, request: Request, pk):
        book_id = self.kwargs['pk']
        book_data = request.data
        updated_book = update_book_use_case.execute(book_id, book_data)
        serializer = self.serializer_class(updated_book)
        return Response(serializer.data, status=status.HTTP_200_OK)

        # book = Book.objects.get(pk=pk)
        # srz_data = BookSerializer(instance=book, data=request.data, partial=True)
        # if srz_data.is_valid():
        #     srz_data.save()
        #     return Response(data=srz_data.data, status=status.HTTP_200_OK)
        # return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BookCreateAPIView(generics.CreateAPIView):
    serializer_class = BookSerializer


class BookRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Specify allowed HTTP methods (only GET)

    def get_object(self):
        # Get the book ID from the URL parameter "pk"
        book_id = self.kwargs.get('pk')

        # Use the GetBookByIDUseCase to retrieve the book by ID
        book = get_book_by_id_use_case.execute(book_id)

        # If the book is not found, you can handle the exception or return None
        if book is None:
            raise Http404("Book not found")

        return book
