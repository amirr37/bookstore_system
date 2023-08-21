from django.urls import path
from api import views
from api.views import BookListView

urlpatterns = [
    path('', BookListView.as_view(), name='book-list-api'),

]
