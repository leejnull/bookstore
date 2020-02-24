from .storage import *


def set_crawling_book(title, author, website):
    s_set('{0}|{1}|{2}'.format(title, author, website), True, 1*60*60)
