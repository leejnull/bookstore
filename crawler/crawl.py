from utils import requestor
from utils.logger import logger
from bs4 import BeautifulSoup
from book import models as book_models
from crawler import models as crawler_models
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
            exists = book_models.Book.objects.filter(title=title, author=author).exists()

            res.append({
                'title': title,
                'intro': intro,
                'author': author,
                'category': category,
                'img_url': image,
                'website_id': website_id,
                'website_title': website_title,
                'book_id': novel_id,
                'exists': exists
            })
    else:
        logger.error('返回页面为空|%s|%s', search_url, book_name)

    return res


def crawling_book_from_biquge(book_id, book_url, website_id, domain_url):
    url = '{0}{1}{2}'.format(book_url, book_id, '/')
    html = requestor.get(url)
    if html:
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find('div', id='info').h1.string.strip()
        img = soup.find('div', id='fmimg').img['src'].strip()
        author_string = soup.find('div', id='info').p.string
        state_string = ''.join(soup.find('div', id='info').p.next_sibling.next_sibling.strings)
        finished = '连载中' not in state_string
        author = re.match(r'.+：(.+)', author_string).group(1).strip()
        intro = soup.find('div', id='intro').string.strip()
        category = soup.find('meta', property='og:novel:category')['content']

        try:
            category_id = book_models.Category.objects.get(name=category).id
        except book_models.Category.DoesNotExist:
            category_id = book_models.Category.objects.create(name=category).id

        try:
            book = book_models.Book.objects.create(
                title=title,
                image_url=img,
                finished=finished,
                author=author,
                intro=intro,
                category_id=category_id,
                website_id=website_id,
                related_id=book_id
            )
            logger.info("创建Book成功")
            try:
                record = crawler_models.CrawlingRecord.objects.create(book_id=book.id,
                                                                      status=crawler_models.CrawlingRecord.Status.CRAWLING_UN)
            except Exception as e:
                logger.error('创建爬虫记录出错|%s', e)
                return
            chapters = soup.find_all('dd')
            for i, chapter in enumerate(chapters):
                if i == 0:
                    record.status = crawler_models.CrawlingRecord.Status.CRAWLING_PROCESSING
                chapter_url = domain_url + chapter.a['href']
                crawling_chapter_from_biquge(chapter_url, book, record)
            record.status = crawler_models.CrawlingRecord.Status.CRAWLING_SUCCESS
        except Exception as e:
            logger.error("创建Book出错|%s", e)
    else:
        logger.warning('该书籍ID找不到对应数据|%s', book_id)


def crawling_chapter_from_biquge(chapter_url, book, record):
    html = requestor.get(chapter_url)
    if html:
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find('h1').string.strip()
        contents = soup.find('div', id='content').strings
        text = ''
        words = 0
        for content in contents:
            text += content.strip()
            words += len(text)
            text += '\n'

        try:
            content = book_models.Content.objects.create(content=text)
        except Exception as e:
            logger.error('创建Content出错|%s', e)
            record.status = crawler_models.CrawlingRecord.Status.CRAWLING_FAILURE
            return

        try:
            chapter = book_models.Chapter.objects.create(
                title=title,
                book_id=book.id,
                content_id=content.id,
                words=words,
            )
            logger.info('创建Chapter成功|%s', chapter)
        except Exception as e:
            logger.error('创建Chapter出错|%s', e)
            record.status = crawler_models.CrawlingRecord.Status.CRAWLING_FAILURE
