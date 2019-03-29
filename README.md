# Создание PDF-сертификатов по CSV grade report

## Требования
* Python 3+ (версия 2 не поддерживается)

## Установка
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

## Запуск

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
