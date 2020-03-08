from django.db import models
from crawler import crawl
from book import models as book_models
from utils.logger import logger
from utils.conventor import ts_from_dt


class Website(models.Model):
    title = models.CharField(max_length=32, unique=True)
    domain = models.CharField(max_length=128)
    search_url = models.CharField(max_length=256, default='')
    detail_url = models.CharField(max_length=256, default='')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title
        }

    def is_biquge(self):
        return self.title == "笔趣阁"

    def search_book(self, book_name):
        if self.is_biquge():
            return crawl.search_book_from_biquge(book_name, self.search_url, self.id, self.title)

    def crawling_book(self, book_id):
        if self.is_biquge():
            crawl.crawling_book_from_biquge(book_id, self.detail_url, self.id, self.domain)


class CrawlingRecord(models.Model):
    class Status(models.IntegerChoices):
        CRAWLING_UN = 0
        CRAWLING_PROCESSING = 1
        CRAWLING_SUCCESS = 2
        CRAWLING_FAILURE = 3
    book_id = models.IntegerField()
    status = models.IntegerField(choices=Status.choices, default=0)
    create_dt = models.DateTimeField(auto_created=True, auto_now=True)

    def to_dict(self):
        try:
            book = book_models.Book.objects.get(id=self.book_id)
        except book_models.Book.DoesNotExist:
            logger.error('爬虫记录获取关联书籍出错|%s', self.book_id)
            return None
        status_desc = ''
        if self.status == CrawlingRecord.Status.CRAWLING_UN:
            status_desc = '未爬取'
        elif self.status == CrawlingRecord.Status.CRAWLING_PROCESSING:
            status_desc = '爬取中',
        elif self.status == CrawlingRecord.Status.CRAWLING_SUCCESS:
            status_desc = '爬取成功'
        elif self.status == CrawlingRecord.Status.CRAWLING_FAILURE:
            status_desc = '爬取失败'

        result_dict = {'status': self.status,
                       'status_desc': status_desc,
                       'create_dt': ts_from_dt(self.create_dt)}
        result_dict.update(book.to_dict())
        return result_dict
