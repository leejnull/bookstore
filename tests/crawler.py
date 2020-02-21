from utils import requestor
from bs4 import BeautifulSoup

base_url = 'https://www.biquge.com.cn/search.php?q='


def crawling():
    url = base_url + '诡秘之主'
    html = requestor.get(url)
    if html:
        soup = BeautifulSoup(html, 'lxml')
        result_list = soup.find_all(class_='result-item')
        for result in result_list:
            image = result.find(class_='result-game-item-pic-link').img['src']
            title = result.find(class_='result-game-item-title-link').span.string
            intro = result.find(class_='result-game-item-desc').string
            item_info_list = result.find_all(class_='result-game-item-info-tag')
            author = item_info_list[0].find_all('span')[-1].string
            category = item_info_list[1].find_all('span')[-1].string
            print(category)



if __name__ == '__main__':
    crawling()

