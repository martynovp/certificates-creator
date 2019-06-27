# Создание PDF-сертификатов по CSV grade report

## Требования
* Python 3+ (версия 2 не поддерживается)

## Установка для Linux & MacOS
1. `virtualenv -p python3 venv`
2. `source venv/bin/activate`
3. Устанавливаем python зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Для корректной работы библиотеки `pdfkit` требуется установить пакет `wkhtmltopdf`:
   ```bash
   sudo apt-get install wkhtmltopdf  
   ```
   или же на MacOS:
   ```bash
   brew install Caskroom/cask/wkhtmltopdf 
   ```

## Установка для Windows

Установить python3.6.7 (с добавлением PATH и установкой pip - галочки при установке)
https://www.python.org/downloads/release/python-367/

Установить wkhtmltopdf
https://wkhtmltopdf.org/downloads.html

Прописать пути к python и wkhtmltopdf в Environment Variables
![Alt text](img/Win_env.png?raw=true "Title")

Открыть cmd
Убедиться, что Environment Variables корректно подцепились:
```bash
$ C:\Users> python --version
Python 3.6.7
```

Установить pdfkit
```bash
$ C:\Users> pip install pdfkit==0.6.1 --user
```


## Запуск

В консоли перейти в корневую папку скрипта
```bash
$ cd /path/to/root/of/certificate-creator
```

Внутри папки:
```bash
$ python convert.py -h
usage: convert.py [-h] [--json JSON] csv

Генератор сертификатов по CSV файлу

positional arguments:
  csv          путь к CSV файлу

optional arguments:
  -h, --help   show this help message and exit
  --json JSON  путь к настройкам в json формате
```

Пример:

```bash
$ python convert.py test.csv
$ python convert.py test.csv --json custom_config.json
```

## Настройки

Настройки скрипта корректируются через JSON конфиг:

```javascript
{
    "path_to_background": "background.png", /* путь к подложке в папке шаблона */
    "path_to_template": "template/index.html", /* путь HTML-шаблону */ 
    "path_to_result_dir": "result", /* путь директории куда сохранять PDF-ки */
    "template_variables": { /* константы для шаблона */
    	"course_name": "Теория игр", /* название курса */
    	"course_volume": "3 з.е.", /* объем курса */
    	"course_link": "test.ru/course/mipt/GAMETH", /* ссылка на курс */
    	"course_num": "V001", /* номер курса */
    	"lector_title": "Проректор МФТИ по учебной работе и довузовской подготовке", /* должность лектора */
    	"lector_fio": "Иванов Иван Иванович" /* ФИО лектора */
    },
    "grade_for_3": 60, /* минимальный балл на удовлетворительно */
    "grade_for_4": 80, /* минимальный балл на хорошо */
    "grade_for_5": 95, /* минимальный балл на отлично */
    "min_grade_for_exam": 0.1, /* минимальный балл за экзамен (в контексте всего курса) */
    "title_row_for_exam": "Final Exam (Avg)", /* название столбца с экзаменом */
    "cert_date": "now", /* дата выдачи сертификата: now - берётся текущая дата */
    "cert_num_from": 1, /* стартовый номер сертификата, с которого начинается генерация */
    "cert_options": { /* опции генерации сертификата, подробнее см. https://wkhtmltopdf.org/usage/wkhtmltopdf.txt */
    	"margin-top": "0",
    	"margin-right": "0",
    	"margin-bottom": "0",
    	"margin-left": "0",
    	"encoding": "UTF-8",
    	"page-width": "1280px",
    	"page-height": "900px",
    	"quiet": ""
	}
}

```
