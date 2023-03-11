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

- `book_folder`, `b` - Путь для сохранения книг (по умолчанию - books);
- `book_images`, `i`, Путь для сохранения картинок (по умолчанию - images); 
- `book_json`, `j`, Путь для сохранения json (по умолчанию - json);
- `skip_imgs` - Пропускать загрузку картинок?;
- `skip_txt` - Пропускать загрузку книги?;
- `json_path`, `jp` - Путь сбора данных для .json файлов.

`python parse_tululu_category.py --start_page --end_page`

Пример:

- Загрузка 34 страницы:

`python parse_tululu_category.py 34 35`

- Загрузка первой страницы в папки: `books`, `images`, `json`:

`python parse_tululu_category.py 1 2 -b books -i images -j json`

- Просмотр информации о книгах без загрузки картинок и книг на 4 и 5 странице:

`python parse_tululu_category.py 4 6 --skip_imgs --skip_txt`
