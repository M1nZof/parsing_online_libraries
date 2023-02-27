import os

import requests
from requests import HTTPError


def check_for_redirect(response):
    if response.history:
        raise HTTPError


def download_book():
    for id in range(1, 11):
        url = f'https://tululu.org/txt.php?id={id}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            with open(os.path.join('books', f'book{id}.txt'), 'w') as book_file:
                book_file.write(response.text)
        except HTTPError:
            continue


def creating_books_directory():
    if not os.path.exists('books'):
        os.mkdir('books')


if __name__ == '__main__':
    creating_books_directory()
    download_book()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
