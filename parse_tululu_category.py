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
    parser.add_argument('--dest_folder', '-d',
                        help='Путь для сохранения книг, картинок, json (указывается через пробел)',
                        type=str, default='books_images_json')
    parser.add_argument('--skip_imgs', '-i', help='Пропускать загрузку картинок? (1/0)', type=int, default=0)
    parser.add_argument('--skip_txt', '-t', help='Пропускать загрузку книги? (1/0)', type=int, default=0)
    parser.add_argument('--json_path', '-j', help='Путь сбора данных для .json файлов', type=str, default='-')

    args = parser.parse_args()
    folders = args.dest_folder.split('_')

    for folder_name in folders:
        os.makedirs(folder_name, exist_ok=True)

    for page in range(args.start_page, args.end_page):
        genre_url = 'https://tululu.org/l55/'
        page_url = urljoin(genre_url, f'{page}/')
        response = requests.get(page_url)
        response.raise_for_status()
        check_for_redirect(response)

        soup = BeautifulSoup(response.text, 'lxml')
        books_on_page = soup.select('#content .d_book .bookimage a')

        for book_tag in books_on_page:
            book_endlink = book_tag['href']
            book_url = urljoin(genre_url, book_endlink)
            book_id = book_endlink.replace('/', '').replace('b', '')
            book_text_url = f'https://tululu.org/txt.php?id={book_id}/'

            try:
                book_page_response = requests.get(book_url)
                book_page_response.raise_for_status()
                check_for_redirect(book_page_response)

                title, author, genres, comments, image_link = parse_book_page(book_page_response)
                if os.path.exists(args.json_path):
                    book_json = {
                        'title': title,
                        'author': author,
                        'genres': genres,
                        'comments': comments,
                        'image_link': image_link
                    }

                    with open('books.json', 'a') as file:
                        json.dump(book_json, file, indent=4, ensure_ascii=False)

                if args.skip_txt == 0:
                    download_txt(book_text_url, book_id, title)

                if args.skip_imgs == 0:
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
