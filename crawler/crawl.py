from utils import requestor
from utils.logger import logger
from bs4 import BeautifulSoup
from book import models
import re


def search_book_from_biquge(book_name, search_url, website_id, website_title):
    url = search_url + book_name
    html = requestor.get(url)
    res = []
    if html:
        soup = BeautifulSoup(html, 'lxml')
        result_list = soup.find_all(class_='result-item')
        for result in result_list:
            image = result.find(class_='result-game-item-pic-link').img['src']
            href = result.find(class_='result-game-item-pic-link')['href']
            novel_id = re.search(r'/(\d+)/$', href).group(1)
            title = result.find(class_='result-game-item-title-link').span.string
            intro = result.find(class_='result-game-item-desc').string
            item_info_list = result.find_all(class_='result-game-item-info-tag')
            author = item_info_list[0].find_all('span')[-1].string
            category = item_info_list[1].find_all('span')[-1].string
            exists = models.Novel.objects.filter(title=title, author=author).exists()

            res.append({
                'title': title,
                'intro': intro,
                'author': author,
                'category': category,
                'img_url': image,
                'website_id': website_id,
                'website_title': website_title,
                'novel_id': novel_id,
                'exists': exists
            })
    else:
        logger.error('返回页面为空|%s|%s', search_url, book_name)

    return res
