from config.key import TOKEN_KEY, TOKEN_EXPIRE
from utils.decorator import pre_login, post, require_login
from utils.encryption import gen_token, md5
from utils.logger import logger
from utils.response import response_failure, response_success, response_login
from utils import validator
from store import user as store_user
from .models import Account


@pre_login
@post
def login(request):
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
    except (KeyError, TypeError, ValueError):
        logger.error('参数不正确|%s', request.POST)
        return response_failure(message='请求参数错误')

    try:
        account = Account.objects.get(username=username)
    except Account.DoesNotExist:
        logger.warning('找不到用户名|%s', username)
        return response_failure(message='找不到用户名')

    md5_pass = md5(password)
    if account.password != md5_pass:
        logger.warning('该用户名密码错误|%s', password)
        return response_failure(message='该用户名密码错误')

    response = response_success(message='登录成功')
    token = gen_token()
    response.set_cookie(TOKEN_KEY, token, TOKEN_EXPIRE)
    store_user.set_token(token, account.id)
    return response


@require_login
def ping_login(request):
    return response_success('已登录')


def logout(request):
    token = store_user.get_token(request.COOKIES)
    store_user.delete_token(token)
    response = response_success('已登出')
    response.delete_cookie(TOKEN_KEY)
    return response


@post
def register(request):
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
    except (TypeError, KeyError, ValueError):
        logger.error('参数不正确|%s', request.POST)
        return response_failure(message='请求参数错误')

    if not validator.validate_username(username):
        logger.warning('用户名不能少于3位|%s', username)
        return response_failure(message='用户名不能少于3位')

    if not validator.validate_pass(password):
        logger.warning('密码不能为空|%s', password)
        return response_failure(message='密码不能为空')

    if Account.objects.filter(username=username):
        logger.warning('用户名已存在|%s', username)
        return response_failure(message='用户名已存在')
    try:
        password = md5(password)
        account = Account.objects.create(username=username, password=password)
    except Exception as e:
        logger.error('注册失败|%s', e)
        return response_failure(message='注册失败')

    return response_success(message='注册成功', data={
        'id': account.id,
        'username': account.username
    })


@require_login
def get_user_info(request):
    token = store_user.get_token(request.COOKIES)
    account_id = store_user.get_token_account_id(token)
    try:
        account = Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        logger.warning('找不到指定的account|%s', account_id)
        return response_login()

    return response_success(data=account.to_dict())
