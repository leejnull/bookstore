from utils.decorator import post, require_login
from utils.logger import logger
from utils.response import response_failure, response_success
from utils.enums import StatusCode
from config.default_data import NOVEL_CATEGORY
from .models import Category


@require_login
@post
def index(request):
    return response_success(message='请求成功，这是book index页面')


@require_login
@post
def correct_data(request):
    try:
        for category_title in NOVEL_CATEGORY:
            Category.objects.update_or_create(
                name=category_title
            )
    except Exception as e:
        logger.error('未知错误|%s', e)
        return response_failure()

    return response_success()
