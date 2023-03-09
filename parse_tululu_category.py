import argparse
import json
import os
import sys
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests import HTTPError

from main import parse_book_page, download_txt, check_for_redirect, download_image

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Скрипт загрузки книг научной фантастики с сайта https://tululu.org')
    parser.add_argument('start_page', help='С какой страницы начинать скачивание книг', type=int, default=1)
    parser.add_argument('end_page', help='Какой страницей заканчивать скачивание книг', type=int, default=2)
    parser.add_argument('--book_folder', '-b', help='Путь для сохранения книг', type=str, default='books')
    parser.add_argument('--book_images', '-i', help='Путь для сохранения картинок', type=str, default='images')
    parser.add_argument('--book_json', '-j', help='Путь для сохранения json', type=str, default='json')
    parser.add_argument('--skip_imgs', help='Пропускать загрузку картинок?',
                        action='store_true', default=False)
    parser.add_argument('--skip_txt', help='Пропускать загрузку книги?',
                        action='store_true', default=False)
    parser.add_argument('--json_path', '-jp', help='Путь сбора данных для .json файлов', type=str, default='-')

    args = parser.parse_args()

    os.makedirs(args.book_folder, exist_ok=True)
    os.makedirs(args.book_images, exist_ok=True)
    os.makedirs(args.book_json, exist_ok=True)

    book = {}

    for page_number in range(args.start_page, args.end_page):
        genre_url = 'https://tululu.org/l55/'
        page_url = urljoin(genre_url, f'{page_number}/')
        response = requests.get(page_url)
        response.raise_for_status()
        check_for_redirect(response)

        soup = BeautifulSoup(response.text, 'lxml')
        books_on_page = soup.select('#content .d_book .bookimage a')

        for book_tag in books_on_page:
            try:
                book_endlink = book_tag['href']
                book_url = urljoin(genre_url, book_endlink)
                book_id = book_endlink.replace('/', '').replace('b', '')
                book_text_url = f'https://tululu.org/txt.php'

                book_page_response = requests.get(book_url)
                book_page_response.raise_for_status()
                check_for_redirect(book_page_response)

                title, author, genres, comments, image_link = parse_book_page(book_page_response)
                if os.path.exists(args.json_path):
                    book[title] = {
                            'author': author,
                            'genres': genres,
                            'comments': comments,
                            'image_link': image_link
                        }

                if not args.skip_txt:
                    download_txt(book_text_url, book_id, title)

                if not args.skip_imgs:
                    download_image(image_link)

                print(f'Название: {title}\n'
                      f'Автор: {author}\n'
                      f'Жанры: {genres}\n'
                      f'Комментарии: {comments}\n\n')

            except HTTPError:
                print('Ошибка запроса на сервер\n', file=sys.stderr)
            except requests.exceptions.ConnectionError:
                print('Ошибка соединения', file=sys.stderr)
                print('Попытка повторного подключения\n')
                time.sleep(10)

    if os.path.exists(args.json_path):
        with open('books.json', 'a') as file:
            json.dump(book, file, indent=4, ensure_ascii=False)
