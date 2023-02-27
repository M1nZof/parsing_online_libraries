import os
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from requests import HTTPError
from pathvalidate import sanitize_filename


def check_for_redirect(response, check_len=False):
    if check_len:
        if len(response.history) > 1:
            raise HTTPError
    else:
        if response.history:
            raise HTTPError


def download_txt(url, filename, folder='books/'):
    _, book_id = urlparse(url).query.split('=')
    sanitazed_filename = f'{sanitize_filename(filename)}.txt'
    response = requests.get(url)
    response.raise_for_status()

    try:
        check_for_redirect(response, check_len=True)
    except HTTPError:
        return

    with open(os.path.join(folder, f'{book_id}. {sanitazed_filename}'), 'w') as book:
        book.write(response.text)

    return f"{folder}{sanitazed_filename}"


def download_book(book_id):
    book_url = f'https://tululu.org/b{book_id}/'
    book_text_url = f'http://tululu.org/txt.php?id={book_id}'

    response = requests.get(book_url)
    response.raise_for_status()

    try:
        check_for_redirect(response)
    except HTTPError:
        return

    soup = BeautifulSoup(response.text, 'lxml')
    title, _, author = soup.find('h1').text.split('   ')
    download_txt(book_text_url, title)


def creating_books_directory():
    if not os.path.exists('books'):
        os.mkdir('books')


if __name__ == '__main__':
    creating_books_directory()
    for book_id in range(1, 11):
        download_book(book_id)
