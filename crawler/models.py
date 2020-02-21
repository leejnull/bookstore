from django.db import models
from crawler import crawl


class Website(models.Model):
    title = models.CharField(max_length=32, unique=True)
    domain = models.CharField(max_length=128)
    search_url = models.CharField(max_length=256, default="")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title
        }

    def is_biquge(self):
        return self.title == "笔趣阁"

    def search_book(self, book_name):
        if self.is_biquge():
            return crawl.search_book_from_biquge(book_name, self.search_url, self.id)
