from .storage import *


def start_crawling_book(book_id, website_id):
    s_set('{0}|{1}'.format(book_id, website_id), '0', 1*60*60)


def finish_crawling_book(book_id, website_id):
    s_set('{0}|{1}'.format(book_id, website_id), '1', 1*60*60)


def failure_crawling_book(book_id, website_id):
    s_set('{0}|{1}'.format(book_id, website_id), '-1', 1*60*60)


def get_book_state(book_id, website_id):
    return s_get('{0}|{1}'.format(book_id, website_id))
