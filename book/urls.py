from django.urls import path
from book import views as book_api


urlpatterns = [
    path('', book_api.index, name='book_index'),

    path('correct_data', book_api.correct_data)
]
