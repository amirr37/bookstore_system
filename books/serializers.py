from rest_framework import serializers

from books.models import Author, Book, Genre


class AuthorSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()

    def get_city(self, author):
        return author.birthplace.name if author.birthplace else None

    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'city']


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Book
        fields = ['title', 'publication_date', 'isbn', 'price', 'genre', 'authors']

    def validate_title(self, title):
        if len(title) > 200:
            raise serializers.ValidationError("Title length must be 200 characters or less.")
        return title

    def create(self, validated_data):
        # book = Book(title=validated_data.get('title'), publication_date=validated_data.get('publication_date'),
        #             isbn=validated_data.get('isbn'), price=validated_data.get('price'),
        #             genre_id=Genre.objects.get(title=validated_data.get('genre')).id, )
        # book.save()
        # for id in validated_data.get('authors'):
        #     author = Author.objects.get(id=id)
        #     book.authors.add(author)
        # book.save()
        # return book
        author_ids = validated_data.pop('authors', [])
        genre_id = Genre.objects.get(title=validated_data.pop('genre')).id

        book = Book.objects.create(**validated_data, genre_id=genre_id)
        book.authors.set(author_ids)
        return book
