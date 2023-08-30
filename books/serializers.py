from rest_framework import serializers
from datetime import date, timedelta

from books.models import Author, Book, Genre


class AuthorSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()

    def get_city(self, author):
        return author.birthplace.name if author.birthplace else None

    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'city']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'publication_date', 'isbn', 'price', 'genre', 'authors']

    def validate_publication_date(self, value):
        tomorrow = date.today() + timedelta(days=1)
        if value >= tomorrow:
            raise serializers.ValidationError("Publication date must be before tomorrow.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must not be less than zero.")
        return value

    def validate_isbn(self, value):
        if not value.isdigit() or len(value) != 13:
            raise serializers.ValidationError("ISBN must be a 13-digit number.")
        return value

