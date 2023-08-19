from django.db import models
from django.utils.text import slugify


# Create your models here.


class Genre(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='Genre Name')

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    authors = models.CharField(max_length=200, verbose_name='Authors')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, verbose_name='Genre')
    publication_date = models.DateField(verbose_name='Publication Date')
    isbn = models.CharField(max_length=13, verbose_name='ISBN')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    slug = models.SlugField(unique=True, null=False, blank=False, )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
