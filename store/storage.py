from django.core.cache import cache


def s_set(key, value, timeout):
    cache.set(key, value, timeout=timeout)


def s_get(key):
    return cache.get(key)


def s_delete(key):
    cache.delete_pattern(key)


def s_timeout(key):
    """
    获取对应key的过期时间
    :rtype: Number
    """
    return cache.ttl(key)


def s_expire(key, timeout):
    """
    延迟过期时间
    :rtype
    """
    cache.expire(key, timeout=timeout)
