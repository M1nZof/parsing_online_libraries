from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = 'http://tululu.org/l55/'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    parsed_content = soup.find('div', {'id': 'content'}).find('a', {'class': ''})
    book_id = parsed_content['href']
    book_url = urljoin(url, book_id)
    print(book_url)
