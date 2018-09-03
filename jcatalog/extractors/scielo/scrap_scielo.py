# coding: utf-8
from datetime import datetime

import requests
import xlsxwriter

from articlemeta.client import ThriftClient

client = ThriftClient()

doajapi = 'https://doaj.org/api/v1/search/journals/issn:'

collections = requests.get(
    "http://articlemeta.scielo.org/api/v1/collection/identifiers/")

workbook = xlsxwriter.Workbook('scielo.xlsx')
worksheet = workbook.add_worksheet('SciELO Network')

format_date = workbook.add_format({'num_format': 'yyyy-mm-dd'})

today = datetime.now().strftime('%Y-%m-%d')

row = 0
col = 0

for h in [
        'extraction_date',
        'acronym',
        'collection',
        'issn',
        'title_scielo',
        'status'
]:

    worksheet.write(row, col, h)
    col += 1

row = 1

for collection in collections.json():

    print(collection['acron'])

    acro = collection['acron']

    journals = client.journals(collection=acro)

    for journal in journals:

        col = 0

        # scielo issn
        issn = journal.scielo_issn

        j = client.journal(collection=acro, code=issn)

        if j:

            worksheet.write(row, col, today, format_date)
            col += 1

            worksheet.write(row, col, acro)
            col += 1

            worksheet.write(row, col, "SciELO " + collection['original_name'])
            col += 1

            worksheet.write(row, col, issn)
            col += 1

            worksheet.write(row, col, journal.title)
            col += 1

            worksheet.write(row, col, journal.current_status)
            col += 1

            row += 1


workbook.close()
