from .storage import *
from config import key


def set_token(token, account_id):
    s_set(token, account_id, key.TOKEN_EXPIRE)


def get_token(cookie):
    return cookie.get(key.TOKEN_KEY)


def get_token_account_id(token):
    account_id = s_get(token)
    return account_id


def delete_token(token):
    s_delete(token)


def expire_token(token):
    """
    延长token过期时间，如果剩余时间少于一个TOKEN_TTL，那么再延长两个TTL
    :param token:
    """
    ttl = s_timeout(token)
    if ttl < key.TOKEN_TTL:
        s_expire(token, key.TOKEN_TTL*2)
