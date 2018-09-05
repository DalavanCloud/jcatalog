# coding: utf-8
from datetime import datetime

import requests
import xlsxwriter

from articlemeta.client import ThriftClient

client = ThriftClient()

doajapi = 'https://doaj.org/api/v1/search/journals/issn:'

collections = requests.get(
    "http://articlemeta.scielo.org/api/v1/collection/identifiers/")

workbook = xlsxwriter.Workbook('doajapi.xlsx')
worksheet = workbook.add_worksheet('SciELO DOAJ')

format_date = workbook.add_format({'num_format': 'yyyy-mm-dd'})

today = datetime.now().strftime('%Y-%m-%d')

row = 0
col = 0

for h in [
        'extraction_date',
        'acronym',
        'issn',
        'title_scielo',
        'status',
        'result',
        'title_doaj',
        'provider',
        'publisher',
        'country',
        'last_updated',
        'url']:

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
            r = requests.get(doajapi + '%s' % issn)
            print(r.headers['Link'])

            doaj = r.json()
            print(doaj['total'])

            result = 0
            title_doaj = None
            provider = None
            publisher = None
            country = None
            last_up = None

            if doaj['total'] > 0:
                result = 1

                if 'results' in doaj:
                    if 'title' in doaj['results'][0]['bibjson']:
                        title_doaj = doaj['results'][0]['bibjson']['title']

                    if 'provider' in doaj['results'][0]['bibjson']:
                        provider = doaj['results'][0]['bibjson']['provider']

                    if 'publisher' in doaj['results'][0]['bibjson']:
                        publisher = doaj['results'][0]['bibjson']['publisher']

                    if 'country' in doaj['results'][0]['bibjson']:
                        country = doaj['results'][0]['bibjson']['country']

                    if 'last_updated' in doaj['results'][0]:
                        last_up = doaj['results'][0]['last_updated'][0:10]

            worksheet.write(row, col, today, format_date)
            col += 1

            worksheet.write(row, col, acro)
            col += 1

            worksheet.write(row, col, issn)
            col += 1

            worksheet.write(row, col, journal.title)
            col += 1

            worksheet.write(row, col, journal.current_status)
            col += 1

            worksheet.write(row, col, result)
            col += 1

            worksheet.write(row, col, title_doaj)
            col += 1

            worksheet.write(row, col, provider)
            col += 1

            worksheet.write(row, col, publisher)
            col += 1

            worksheet.write(row, col, country)
            col += 1

            worksheet.write(row, col, last_up, format_date)
            col += 1

            worksheet.write(row, col, doajapi + issn)
            col += 1

            row += 1


workbook.close()
