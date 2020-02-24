from django.urls import path
from crawler import views as crawler_api


urlpatterns = [
    path('', crawler_api.index, name='crawler_index'),
    path('get_search_options', crawler_api.get_search_options, name='search_options'),
    path('search_book', crawler_api.search_book, name='search_book'),
    path('crawling_book', crawler_api.crawling_book, name='crawling_book'),

    path('correct_data', crawler_api.correct_data, name='correct_data')
]
