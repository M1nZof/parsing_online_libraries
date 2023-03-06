import argparse
import os
import sys
import time
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup
from requests import HTTPError

from main import parse_book_page, download_txt, check_for_redirect, download_image

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Скрипт загрузки книг научной фантастики с сайта https://tululu.org')
    parser.add_argument('start_page', help='С какой страницы начинать скачивание книг', type=int, default=1)
    parser.add_argument('end_page', help='Какой страницей заканчивать скачивание книг', type=int, default=2)

    args = parser.parse_args()

    os.makedirs('books', exist_ok=True)
    os.makedirs('images', exist_ok=True)

    for page in range(args.start_page, args.end_page):
        genre_url = 'http://tululu.org/l55/'
        page_url = urljoin(genre_url, str(page))
        response = requests.get(page_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        parsed_content = soup.select('#content .d_book .bookimage a')

        for book_tag in parsed_content:
            book_endlink = book_tag['href']
            book_url = urljoin(genre_url, book_endlink)
            book_id = book_endlink.replace('/', '').replace('b', '')
            book_text_url = f'https://tululu.org/txt.php?id={book_id}/'

            try:
                book_page_response = requests.get(book_url)
                book_page_response.raise_for_status()

                title, author, genres, comments, image_link = parse_book_page(book_page_response)

                download_txt(book_text_url, book_id, title)

                download_image(image_link)

                print(f'Название: {title}\n'
                      f'Автор: {author}\n'
                      f'Жанры: {genres}\n'
                      f'Комментарии: {comments}\n\n')

            except TypeError:
                print('Книга отсутствует в свободном доступе\n', file=sys.stderr)
                continue
            except HTTPError:
                print('Ошибка запроса на сервер\n', file=sys.stderr)
            except requests.exceptions.ConnectionError:
                print('Ошибка соединения', file=sys.stderr)
                print('Попытка повторного подключения\n')
                time.sleep(10)
