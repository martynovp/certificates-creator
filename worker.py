# -*- coding: utf-8 -*-

import argparse
import json
import pdfkit
import re
import sys

parser = argparse.ArgumentParser(description='Worker для генерации сертификата по HTML шаблону')
parser.add_argument('html_path', help='путь к HTML шаблону')
parser.add_argument('--json', default='config.json', help='путь к настройкам в json формате')
args = parser.parse_args()

f = open(args.json, encoding="utf8")
cnf_str = f.read()
f.close()

try:
    cnf = json.loads(cnf_str)
except:
    raise Exception("JSON файл содержит невалидный JSON")

f = open(args.html_path, encoding="utf8")
html_content = f.read()
f.close()

match = re.findall("<title>(.*?)</title>", html_content)
cert_result_path = match[0]

with open(args.html_path, encoding="utf8") as f:
    pdfkit.from_file(f, cert_result_path, options=cnf['cert_options'])
