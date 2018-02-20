# coding: utf-8
'''
Generates a contact list of SciELO journal editors.
'''
import sys

import xlsxwriter
from articlemeta.client import ThriftClient


scielo_fields = [
 'scielo_issn',
 'title',
 'current_status',
 'first_year',
 'collection_acronym',
 'editor_email',
 'publisher_name',
 'publisher_country',
 'publisher_city',
 'url()']

workbook = xlsxwriter.Workbook('output/invite_scielo_20.xlsx')
worksheet = workbook.add_worksheet('scielo_doaj')

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

for journal in client.journals():
    print(journal.scielo_issn)
    col = 0

    for label in scielo_fields:
        jdata = None
        if label == 'first_year':
            try:
                jdata = eval('journal.'+label)
                worksheet.write(row, col, str(jdata), format_date)
            except ValueError:
                pass
        else:
            if label == 'publisher_country':
                if hasattr(journal, label) and type(journal.publisher_country) == tuple:
                    worksheet.write(row, col, journal.publisher_country[1])
            else:
                jdata = eval('journal.'+label)
                worksheet.write(row, col, str(jdata))

        col += 1
    row += 1

# Grava planilha Excel
try:
    workbook.close()
except IOError as e:
    print(e)
    sys.exit(1)
