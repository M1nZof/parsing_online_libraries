# parsing_online_libraries

## Описание работы

Скрипт загрузки книг с сайта `https://tululu.org`

## Как установить

Установка необходимых библиотек

`pip install requirements.txt`

## Как пользоваться

Требуемые аргументы:

- `--start_id` - начальный ID книги
- `--end_id` - конечный ID книги

`python main.py --start_id --end_id`

Пример:

`python main.py 1 15`

Скрипт скачает книги, которые доступны с 1 по 15 ID.
