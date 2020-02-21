import requests
from utils.logger import logger


def get(url, headers=None):
    try:
        custom_headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, '
                                        'like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
        if headers:
            custom_headers = headers
        logger.info('开始抓取网页|%s|%s', url, custom_headers)
        resp = requests.get(url, headers=custom_headers)
        if resp.status_code == 200:
            return resp.text
        else:
            logger.warning('抓取网页状态码异常|%s', resp.status_code)
            return None
    except requests.RequestException as e:
        logger.warning('抓取网页其它异常|%s', e)
        return None


def download_image(url, filename, headers=None):
    try:
        custom_headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, '
                                        'like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
        if headers:
            custom_headers = headers
            custom_headers['user-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, ' \
                                           'like Gecko) Chrome/79.0.3945.117 Safari/537.36'
        resp = requests.get(url, headers=custom_headers)
        if resp.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(resp.content)
            return True
        else:
            logger.warning('下载图片状态码异常|%s', resp.status_code)
            return False
    except requests.RequestException as e:
        logger.warning('下载图片其它异常|%s', resp.status_code)
        return False
