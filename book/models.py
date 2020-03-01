from django.db import models
from utils.logger import logger
from crawler.models import Website


class Book(models.Model):
    title = models.CharField(max_length=128)
    intro = models.CharField(max_length=258)
    author = models.CharField(max_length=16)
    category_id = models.IntegerField()
    finished = models.BooleanField(default=False)
    image_url = models.CharField(max_length=128)
    website_id = models.IntegerField(null=True)
    related_id = models.IntegerField(null=True)

    class Meta:
        unique_together = (('title', 'author'),)

    def get_category(self):
        try:
            category = Category.objects.get(id=self.category_id)
        except Category.DoesNotExist:
            logger.error('找不到category|%s', self.category_id)
            category = None
        return category

    def get_website(self):
        try:
            website = Website.objects.get(id=self.website_id)
        except Website.DoesNotExist:
            logger.error('找不到website|%s', self.website_id)
            website = None
        return website

    def to_dict(self):
        category = self.get_category()
        website = self.get_website()
        return {
            'title': self.title,
            'intro': self.intro,
            'author': self.author,
            'category': category.name if category else '',
            'image_url': self.image_url,
            'website': website.title if website else '',
            'finished': self.finished
        }


class Chapter(models.Model):
    title = models.CharField(max_length=256)
    book_id = models.IntegerField()
    content_id = models.IntegerField()
    is_delete = models.BooleanField(default=False)
    words = models.IntegerField()
    create_time = models.DateTimeField(auto_created=True)
    update_time = models.DateTimeField(null=True)

    def __str__(self):
        return '{0}|{1}|{2}|{3}'.format(self.title, self.book_id, self.content_id, self.words)


class Content(models.Model):
    content = models.TextField()


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
