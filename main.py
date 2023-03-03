import os
import argparse
import sys
import time
import urllib

from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup
from requests import HTTPError
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise HTTPError


def download_txt(url, filename, folder='books/'):
    _, book_id = urlparse(url).query.split('=')
    raw_book_id = book_id.replace('/', '')
    sanitazed_filename = f'{sanitize_filename(filename)}.txt'
    response = requests.get(url)
    response.raise_for_status()

    with open(os.path.join(folder, f'{raw_book_id}. {sanitazed_filename}'), 'wt', encoding='utf-8') as book:
        book.write(response.text)


def download_book(book_id, title):
    book_url = f'https://tululu.org/b{book_id}/'
    book_text_url = f'https://tululu.org/txt.php?id={book_id}/'

    response = requests.get(book_url)
    response.raise_for_status()

    return book_text_url, title


def download_image(image_link, book_id):
    response = requests.get(image_link)
    response.raise_for_status()

    image_name = urlparse(image_link).path.split('/')[2]

    with open(os.path.join('images', image_name), 'wb') as image:
        image.write(response.content)


def parse_book_image(soup, book_url):
    image_tag = soup.find('div', {'class': 'bookimage'}).select('img')
    image_endlink = image_tag[0]['src']
    image_link = urljoin(book_url, image_endlink)

    return image_link


def parse_page_comments(soup):
    comment_tag = soup.find_all('div', {'class': 'texts'})

    comments = []
    for comment_html in comment_tag:
        comment = comment_html.find_next('span', {'class': 'black'}).text
        comments.append(comment)

    return comments


def parse_book_genres(soup):
    genres_tag = soup.find('span', {'class': 'd_book'}).find_all('a')

    return [genre.text for genre in genres_tag]


def parse_book_page(book_page):
    soup = BeautifulSoup(book_page.text, 'lxml')
    title, _, author = soup.find('h1').text.split('   ')

    image_link = parse_book_image(soup, book_page.url)
    genres = parse_book_genres(soup)
    comments = parse_page_comments(soup)

    return title, author, genres, comments, image_link


def download_book_page(book_id):
    book_url = f'https://tululu.org/b{book_id}/'
    response = requests.get(book_url)
    response.raise_for_status()

    return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Скрипт загрузки книг с сайта https://tululu.org')
    parser.add_argument('start_id', help='С какого ID начинать скачивание книг', type=int)
    parser.add_argument('end_id', help='Каким ID заканчивать скачивание книг', type=int)

    args = parser.parse_args()

    os.makedirs('books', exist_ok=True)
    os.makedirs('images', exist_ok=True)

    for book_id in range(args.start_id, args.end_id):
        try:
            book_page = download_book_page(book_id)
            title, author, genres, comments, image_link = parse_book_page(book_page)

            book_text_url, title = download_book(book_id, title)
            download_txt(book_text_url, title)

            download_image(image_link, book_id)

            print(f'Название: {title}\n'
                  f'Автор: {author}\n'
                  f'Жанры: {genres}\n'
                  f'Комментарии: {comments}\n\n')

        except HTTPError:
            print('Книга отсутствует в свободном доступе\n', file=sys.stderr)
            continue
        except requests.exceptions.ConnectionError:
            print('Ошибка соединения', file=sys.stderr)
            print('Попытка повторного подключения\n')
            time.sleep(10)
