from .response import response_failure, response_login
from store import user
from config import key


def params(*args):
    def check_params(func):
        def in_func(request):
            p = []
            for val in args:
                param = request.POST.get(val, 100)
                if param == 100:
                    return response_failure(message='参数错误，需要参数 %s' % val)
                else:
                    p.append(param)
            return func(request, p)
        return in_func
    return check_params


def get(func):
    def in_func(request):
        if request.method == 'GET':
            return func(request)
        else:
            return response_failure(message='请使用GET请求')
    return in_func


def post(func):
    def in_func(request):
        if request.method == 'POST':
            return func(request)
        else:
            return response_failure(message='请使用POST请求')
    return in_func


def pre_login(func):
    """
    登录前准备工作：1.清空cookie里的token
    :rtype: func
    """
    def wrapper(request):
        token = request.COOKIES.get(key.TOKEN_KEY)
        if token:
            user.delete_token(token)
        return func(request)
    return wrapper


def require_login(func):
    def wrapper(request):
        token = user.get_token(request.COOKIES)
        if not token:
            return response_login()
        if not user.get_token_account_id(token):
            return response_login()
        user.expire_token(token)
        return func(request)

    return wrapper
