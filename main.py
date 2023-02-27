import os

import requests


def download_book():
    os.mkdir('books')
    for id in range(1, 11):
        url = f'https://tululu.org/txt.php?id={id}'
        response = requests.get(url)
        response.raise_for_status()
        with open(os.path.join('books', f'book{id}.txt'), 'w') as book_file:
            book_file.write(response.text)


if __name__ == '__main__':
    download_book()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
