# parsing_online_libraries

## main.py

### Описание работы

Скрипт загрузки книг с сайта `https://tululu.org`

### Как установить

Установка необходимых библиотек

`pip install requirements.txt`

### Как пользоваться

Требуемые аргументы:

- `--start_id` - начальный ID книги
- `--end_id` - конечный ID книги

`python main.py --start_id --end_id`

Пример:

`python main.py 1 15`

## parse_tululu_category.py

### Описание работы

Скрипт загрузки книг с сайта `https://tululu.org` в жанре научной фантастики

### Как установить

Установка необходимых библиотек

`pip install requirements.txt`

### Как пользоваться

Требуемые аргументы:

- `--start_page` - начальная страница с книгами
- `--end_page` - конечная страница с книгами

*На каждой странице находится по 25 книг*

Опциональные аргументы:

- `dest_folder`, `d` - Путь для сохранения книг, картинок, json (указывается через нижнее подчеркивание)
- `skip_imgs`, `i` - Пропускать загрузку картинок?
- `skip_txt`, `t` - Пропускать загрузку книги?
- `json_path`, `j` - Путь сбора данных для .json файлов

`python parse_tululu_category.py --start_page --end_page`

Пример:

- Загрузка 34 страницы:

`python parse_tululu_category.py 34 35`

- Загрузка первой страницы в папки: `books`, `images`, `json`:

`python parse_tululu_category.py 1 2 -d books_images_json`

- Просмотр информации о книгах без загрузки картинок и книг на 4 и 5 странице:

`python parse_tululu_category.py 4 6 -i 1 -t 1`

- Скачивание книг с 20 по 24 страницу сохраняя данные о книгах в директорию со скриптом в файле books.json

`python .\parse_tululu_category.py 20 25 -j .`
