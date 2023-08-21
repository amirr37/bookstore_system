from django.urls import path
from api import views
from api.views import BookListView

urlpatterns = [
    path('api/books/', BookListView.as_view(), name='book-list-api'),

]
