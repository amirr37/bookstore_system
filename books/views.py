from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Book
from .serializers import BookSerializer
from .filters import BookFilter


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


class BookCreateAPIView(generics.CreateAPIView):
    serializer_class = BookSerializer


# class BookCreateAPIView(APIView):
#     def post(self, request: Request):
#         srz_data = BookSerializer(data=request.data)
#         if srz_data.is_valid():
#             # if serializer data is valid , it saves automatically in created method.
#             # srz_data.save()
#             return Response(srz_data.data, status=status.HTTP_201_CREATED)
#         return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDeleteView(APIView):
    def delete(self, request, pk):

        try:
            book = Book.objects.get(pk=pk)
            book.delete()
            return Response(data={'message': 'book deleted'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'message': 'no book with this id'}, status=status.HTTP_400_BAD_REQUEST)


class BookUpdateView(APIView):
    def put(self, request: Request, pk):
        book = Book.objects.get(pk=pk)
        srz_data = BookSerializer(instance=book, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(data=srz_data.data, status=status.HTTP_200_OK)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
