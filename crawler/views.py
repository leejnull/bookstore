from utils.decorator import post, require_login
from utils.logger import logger
from utils.response import response_failure, response_success
from crawler.models import Website
from config.default_data import WEBSITES


@require_login
@post
def index(request):
    return response_success(message='请求成功，这是crawler index页面')


@require_login
def get_search_options(request):
    websites = Website.objects.all()
    options = []
    for website in websites:
        options.append(website.to_dict())
    return response_success(data={
        'search_options': options
    })


@require_login
@post
def search_book(request):
    try:
        search_text = request.POST.get('search_text')
        website_id = request.POST.get('website_id')
    except (ValueError, TypeError, IndexError):
        logger.error('参数不正确|%s', request.POST)
        return response_failure(message='请求参数错误')

    try:
        website = Website.objects.get(id=website_id)
    except Website.DoesNotExist:
        logger.error('找不到website|%s', website_id)
        return response_failure(message='找不到指定网站')

    res = website.search_book(search_text)
    return response_success(message='查询书籍成功', data={
        'book_list': res
    })


@require_login
@post
def correct_data(request):
    try:
        for website in WEBSITES:
            Website.objects.update_or_create(
                title=website['title'],
                defaults={
                    'domain': website['domain'],
                    'search_url': website['search_url']
                }
            )
    except Exception as e:
        logger.error('未知错误|%s', e)
        return response_failure()

    return response_success()
