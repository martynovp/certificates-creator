# -*- coding: utf-8 -*-

import argparse
import datetime
import csv
import json
import tempfile
import subprocess
import os
import sys


def rewrite_csv(csv_file, csv_data):
    print('Идет перезапись CSV...')
    with open(csv_file, mode='w') as csv_f:
        csv_f_writer = csv.writer(csv_f, delimiter=',')
        for csv_item in csv_data:
            csv_f_writer.writerow(csv_item)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Генератор сертификатов по CSV файлу')
    parser.add_argument('csv', help='путь к CSV файлу')
    parser.add_argument('--json', default='config.json', help='путь к настройкам в json формате')
    args = parser.parse_args()

    if not os.path.isfile(args.csv):
        raise Exception("CSV файл не найден")
    if not os.path.isfile(args.json):
        raise Exception("JSON файл с настройками не найден")

    f = open(args.json)
    cnf_str = f.read()
    f.close()

    try:
        cnf = json.loads(cnf_str)
    except:
        raise Exception("JSON файл содержит невалидный JSON")

    path_to_template = ''
    path_to_template_dir = ''
    template_content = ''

    if not os.path.isfile(cnf['path_to_template']):
        raise Exception("HTML-шаблон для сертификата не найден")
    else:
        path_to_template = os.path.abspath(cnf['path_to_template'])
        path_to_template_dir = os.path.dirname(path_to_template)
        f = open(path_to_template)
        template_content = f.read()
        f.close()

    path_to_result_dir = cnf['path_to_result_dir']

    if path_to_result_dir:
        if not os.path.isdir(path_to_result_dir):
            raise Exception("Директория для сохранения PDF сертификатов не найдена")
        path_to_result_dir = os.path.realpath(path_to_result_dir)
    else:
        path_to_result_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

    template_variables = cnf['template_variables']
    grade_for_3 = cnf['grade_for_3']
    grade_for_4 = cnf['grade_for_4']
    grade_for_5 = cnf['grade_for_5']
    cert_date = cnf['cert_date']
    if not cert_date or cert_date == 'now':
        cert_date = datetime.datetime.now().strftime('%d.%m.%Y')

    use_full_name = False
    last_name_idx = None
    first_name_idx = None
    second_name_idx = None
    username_idx = 0
    cert_grade_idx = 0
    cert_num_idx = 0
    grade_idx = 0
    start_cert_num_from = int(cnf['cert_num_from'])
    cert_col_exists = True

    data = []
    first = False

    print('Обрабатываем файл: ' + args.csv)

    with open(args.csv) as f:
        reader = csv.reader(f)
        for row in reader:
            if not first:
                first = True
                if 'Certificate Grade' not in row:
                    row.append('Certificate Grade')
                    cert_col_exists = False
                if 'Certificate Num' not in row:
                    row.append('Certificate Num')
                if 'Last Name' in row or 'First Name' in row or 'Second Name' in row:
                    use_full_name = True
                    if 'Last Name' in row:
                        last_name_idx = row.index('Last Name')
                    if 'First Name' in row:
                        first_name_idx = row.index('First Name')
                    if 'Second Name' in row:
                        second_name_idx = row.index('Second Name')
                username_idx = row.index('Username')
                grade_idx = row.index('Grade')
                cert_grade_idx = row.index('Certificate Grade')
                cert_num_idx = row.index('Certificate Num')
            else:
                if not cert_col_exists:
                    row.append('')
                    row.append('')
                else:
                    cert_num_tmp = row[cert_num_idx]
                    if cert_num_tmp:
                        cert_num_int = int(cert_num_tmp.split('-')[1])
                        if cert_num_int >= start_cert_num_from:
                            start_cert_num_from = cert_num_int + 1
            data.append(row)

    if not cert_col_exists:
        rewrite_csv(args.csv, data)
    counter = 1

    for i, item in enumerate(data):
        if i == 0:
            continue
        grade = float(item[grade_idx]) * 100
        if not item[cert_num_idx] and grade_for_3 <= grade:
            with tempfile.NamedTemporaryFile(dir=path_to_template_dir) as temp:
                fio = item[username_idx]
                fio_br = item[username_idx]
                if use_full_name:
                    fio = ''
                    fio_br = ''
                    if last_name_idx is not None and item[last_name_idx] != 'None':
                        fio = fio + item[last_name_idx] + ' '
                        fio_br = fio_br + item[last_name_idx] + ' '
                    if first_name_idx is not None and item[first_name_idx] != 'None':
                        fio = fio + item[first_name_idx] + ' '
                        fio_br = fio_br + item[first_name_idx] + ' '
                    if second_name_idx is not None and item[second_name_idx] != 'None':
                        if fio_br:
                            fio_br = fio_br + '<br />'
                        fio = fio + item[second_name_idx]
                        fio_br = fio_br + item[second_name_idx]

                print(str(counter) + '. Создаём сертификат для пользователя: ' + fio)

                grade_title = "удовлетворительно"
                if grade_for_4 <= grade < grade_for_5:
                    grade_title = "хорошо"
                elif grade_for_5 <= grade:
                    grade_title = "отлично"

                cert_num = '{:05}'.format(start_cert_num_from)
                result_path = os.path.join(path_to_result_dir,
                                           fio + ' ' + template_variables['course_num'] + '-' + cert_num + '.pdf')

                tpl = template_content.replace('{{ fio }}', fio)\
                    .replace('{{ fio_br }}', fio_br)\
                    .replace('{{ course_name }}', template_variables['course_name'])\
                    .replace('{{ course_volume }}', template_variables['course_volume'])\
                    .replace('{{ course_num }}', template_variables['course_num'])\
                    .replace('{{ course_link }}', template_variables['course_link'])\
                    .replace('{{ lector_title }}', template_variables['lector_title'])\
                    .replace('{{ lector_fio }}', template_variables['lector_fio'])\
                    .replace('{{ grade_title }}', grade_title)\
                    .replace('{{ cert_date }}', cert_date)\
                    .replace('{{ cert_num }}', cert_num)\
                    .replace('{{ result_path }}', result_path)\
                    .replace('{{ path_to_template_dir }}', path_to_template_dir + os.sep)

                temp.write(tpl.encode())
                temp.flush()

                subprocess.call(sys.executable + ' worker.py ' + temp.name + ' --json ' + args.json, shell=True)

                data[i][cert_grade_idx] = grade_title
                data[i][cert_num_idx] = template_variables['course_num'] + '-' + cert_num
                start_cert_num_from += 1
                counter += 1

                rewrite_csv(args.csv, data)

    print('Закончили')
