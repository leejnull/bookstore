from utils.decorator import post, require_login
from utils.logger import logger
from utils.response import response_failure, response_success
from crawler.models import Website, CrawlingRecord
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
def crawling_book(request):
    try:
        website_id = request.POST.get('website_id')
        book_id = request.POST.get('book_id')
    except (ValueError, IndexError, TypeError):
        logger.error('参数不正确|%s', request.POST)
        return response_failure(message='请求参数错误')

    try:
        website = Website.objects.get(id=website_id)
    except Website.DoesNotExist:
        logger.error('找不到website|%s', website_id)
        return response_failure(message='找不到指定网站')

    # 异步抓取书籍
    website.crawling_book(book_id)
    return response_success(message='正在爬取书籍中，请去【爬虫管理】查看进度')


@require_login
@post
def get_crawling_books(request):
    """
    获取正在爬取的书籍列表
    :param request:
    filter_rule: 过滤规则 0：全部；1：正在爬取的；2：抓取成功；3：抓取失败
    rank_rule: 排序规则 0：按创建时间从近到远；1：按创建时间从远到近
    :return: {}
    """
    try:
        filter_rule = int(request.POST.get('filter_rule', '0'))
        rank_rule = int(request.POST.get('rank_rule', '0'))
    except (ValueError, IndexError, TypeError):
        logger.error('参数不正确|%s', request.POST)
        return response_failure(message='请求参数错误')

    if filter_rule == 0:
        record_qs = CrawlingRecord.objects.all()
    else:
        record_qs = CrawlingRecord.objects.get(status=filter_rule)

    if rank_rule == 0:
        record_qs = record_qs.order_by('create_dt')
    else:
        record_qs = record_qs.order_by('-create_dt')

    result = []
    for record in record_qs:
        result.append(record.to_dict())
    return result


@require_login
@post
def correct_data(request):
    try:
        for website in WEBSITES:
            obj, created = Website.objects.get_or_create(
                title=website['title'],
                domain=website['domain'],
                detail_url=website['detail_url'],
                search_url=website['search_url']
            )
            if created:
                logger.info('新增Website|%s|%s', website['title'], website['domain'])
            else:
                logger.info('已存在Website|%s|%s', website['title'], website['domain'])
    except Exception as e:
        logger.error('未知错误|%s', e)
        return response_failure()

    return response_success()
