from rest_framework import serializers
from books.models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()

    def get_city(self, author):
        return author.birthplace.name if author.birthplace else None

    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'city']


class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    publication_date = serializers.DateField()
    isbn = serializers.CharField(max_length=13)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    slug = serializers.SlugField()

    genre = serializers.StringRelatedField()  # Display genre title as a string
    # authors = serializers.StringRelatedField(many=True)  # This will display author names as strings
    authors = AuthorSerializer(many=True, read_only=True)

    # def create(self, validated_data):
    #     return Book.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.publication_date = validated_data.get('publication_date', instance.publication_date)
    #     instance.isbn = validated_data.get('isbn', instance.isbn)
    #     instance.price = validated_data.get('price', instance.price)
    #     instance.slug = validated_data.get('slug', instance.slug)
    #     instance.save()
    #     return instance
