import os

import string

import requests as requests

from bs4 import BeautifulSoup


def head():
    homepage = 'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page='
    page_numbers = [str(i) for i in range(1, int(input()) + 1)]
    user_article = input()
    print('Please wait...')
    for number in page_numbers:
        source_dir = os.getcwd()
        os.mkdir(source_dir + f'\Page_{number}')
        os.chdir(source_dir + f'\Page_{number}')
        get_news_links(homepage + number, user_article)
        os.chdir(source_dir)


def get_news_links(url, article):  # subLinks from main url with article tags with exact article
    r = requests.get(url)
    match r.status_code:
        case 200:
            links_list = []
            soup = BeautifulSoup(r.content, 'html.parser')
            news_article_links = soup.find_all('span', {'class': 'c-meta__type'}, text=article)  # Only article tags
            for news_article in news_article_links:
                anchor = news_article.find_parent('article').find('a', {'data-track-action': 'view article'})
                links_list.append(anchor.get('href'))  # subLinks with article tag from parent tags
            links_content(links_list)
        case _:
            return print(f'The URL returned {r.status_code}')


def links_content(links_list, domain='https://www.nature.com'):
    for path in list(links_list):
        r = requests.get(domain + path)
        match r.status_code:
            case 200:
                soup = BeautifulSoup(r.content, 'html.parser')
                title = soup.find('h1').text.strip(string.punctuation).replace(' ', '_')
                source_file = open(f'{title}.txt', 'wb')
                content = soup.find("div", {"class": "c-article-body"}).text.encode().rstrip()  # OSError without this
                source_file.write(content)  # binary string
                source_file.close()
                print(f'{title}.txt\t.\t.\tCreated.')
            case _:
                return print(f'The URL returned {r.status_code}')


if __name__ == '__main__':
    head()
