import os
from urllib.parse import urlparse, urljoin

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
        raise HTTPError

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

    # download_genre(response)

    try:
        download_txt(book_text_url, title)
        download_image(response)
    except HTTPError:
        return

    # download_comments(response)


def download_image(book_response):
    soup = BeautifulSoup(book_response.text, 'lxml')
    image_tag = soup.find('div', {'class': 'bookimage'}).select('img')
    image_endlink = [item['src'] for item in image_tag][0]
    image_name = image_endlink.split('/')[2]
    image_link = urljoin('https://tululu.org', image_endlink)

    response = requests.get(image_link)
    response.raise_for_status()

    with open(os.path.join('images', f'{image_name}'), 'wb') as image:
        image.write(response.content)


def parse_book_image(book_response):
    soup = BeautifulSoup(book_response.text, 'lxml')
    image_tag = soup.find('div', {'class': 'bookimage'}).select('img')
    image_endlink = [item['src'] for item in image_tag][0]
    # image_name = image_endlink.split('/')[2]
    image_link = urljoin('https://tululu.org', image_endlink)

    return image_link

    # response = requests.get(image_link)
    # response.raise_for_status()

    # with open(os.path.join('images', f'{image_name}'), 'wb') as image:
    #     image.write(response.content)



def parse_page_comments(book_response):
    soup = BeautifulSoup(book_response.text, 'lxml')
    comment_tag = soup.find_all('div', {'class': 'texts'})
    # print(comments)
    comments = []
    for comment_html in comment_tag:
        comment = comment_html.find_next('span', {'class': 'black'}).text
        comments.append(comment)

    return comments

    # with open(os.path.join('comments', f'{book_title}.txt'), 'a') as file:
    #     file.write(f'{comment}\n')


def parse_book_genre(book_response):
    soup = BeautifulSoup(book_response.text, 'lxml')
    genre_tag = soup.find('span', {'class': 'd_book'}).find_all('a')

    return [genre.text for genre in genre_tag]


def parse_book_page(book_id):
    book_url = f'https://tululu.org/b{book_id}/'
    response = requests.get(book_url)
    response.raise_for_status()

    try:
        check_for_redirect(response)
    except HTTPError:
        return

    soup = BeautifulSoup(response.text, 'lxml')
    title, _, author = soup.find('h1').text.split('   ')

    genre = parse_book_genre(response)
    comments = parse_page_comments(response)
    # image_link = parse_book_image(response)
    # text = download_txt()

    return title, author, genre, comments


def creating_books_directory(name):
    if not os.path.exists(name):
        os.mkdir(name)


if __name__ == '__main__':
    title, author, genre, comments = parse_book_page(4)
    print(f'{title} | {author} | {genre} | {comments}')

    # creating_books_directory('books')
    # creating_books_directory('images')
    # creating_books_directory('comments')
    # for book_id in range(5, 11):
    #     download_book(book_id)
