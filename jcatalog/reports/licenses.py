# coding: utf-8

import sys

import xlsxwriter

from articlemeta.client import ThriftClient

scielo_fields = [
 'scielo_issn',
 'title',
 'current_status',
 'collection_acronym',
 'publisher_name',
 'admitted_date',
 'year_admitted',
 'license type',
 'url']

workbook = xlsxwriter.Workbook('output/licenses.xlsx')
worksheet = workbook.add_worksheet('scielo_br')

format_date = workbook.add_format({'num_format': 'dd/mm/yyyy'})
wrap_red = workbook.add_format({'text_wrap': False, 'bg_color': '#DC143C'})

# Header
row = 0
col = 0

for h in scielo_fields:
    worksheet.write(0, col, h, wrap_red)
    col += 1

client = ThriftClient()

row = 1

for journal in client.journals(collection='scl'):
    print(journal.scielo_issn)
    col = 0

    year = int(journal.creation_date[0:4])

    if year >= 2015:

        for label in scielo_fields:

            jdata = None

            if label == 'license type':
                jdata = journal.data['v541'][0]['_']

            elif label == 'publisher_name':
                if hasattr(journal, label):
                    jdata = journal.publisher_name[0]

            elif label == 'admitted_date':
                jdata = journal.creation_date

            elif label == 'year_admitted':
                jdata = journal.creation_date[0:4]

            elif label == 'url':
                if hasattr(journal, label):
                    jdata = journal.url()

            else:
                if hasattr(journal, label):
                    jdata = getattr(journal, label)

            worksheet.write(row, col, str(jdata))

            col += 1

        row += 1

# Grava planilha Excel
try:
    workbook.close()
except IOError as e:
    print(e)
    sys.exit(1)
