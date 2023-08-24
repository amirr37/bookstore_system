from rest_framework import serializers

from books.models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()

    def get_city(self, author):
        return author.birthplace.name if author.birthplace else None

    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'city']


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ['title', 'publication_date', 'isbn', 'price', 'genre', 'authors']

    def create(self, validated_data):
        author_data = validated_data.pop('authors')
        book = Book.objects.create(**validated_data)

        for author_item in author_data:
            author_id = author_item['id']
            author = Author.objects.get(id=author_id)
            book.authors.add(author)
        return book

    def update(self, instance, validated_data):
        authors_data = validated_data.pop('authors', [])
        instance = super().update(instance, validated_data)

        instance.authors.clear()
        for author_item in authors_data:
            author_id = author_item['id']
            author = Author.objects.get(id=author_id)
            instance.authors.add(author)
        return instance
