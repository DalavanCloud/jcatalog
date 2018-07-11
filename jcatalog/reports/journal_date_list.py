# coding: utf-8
'''
Generates a contact list of SciELO journal editors.
'''
import sys

import xlsxwriter
from articlemeta.client import ThriftClient

import models

def journal_date_list():
    scielo_fields = [
     'ISSN SciELO',
     'SciELO collection',
     'Publisher country',
     'Title',
     'Status',
     'Creation year',
     'Inclusion year at SciELO',
     'Stopping year at SciELO',
     'Publisher Name',
     'URL']

    workbook = xlsxwriter.Workbook('output/journal_dates_list.xlsx')
    worksheet = workbook.add_worksheet('SciELO')

    format_date = workbook.add_format({'num_format': 'dd/mm/yyyy'})
    wrap_red = workbook.add_format({'text_wrap': False, 'bg_color': '#DC143C'})

    # Header
    row = 0
    col = 0

    for h in scielo_fields:
        worksheet.write(0, col, h, wrap_red)
        col += 1

    row = 1

    query = models.Scielo.objects

    for doc in query:
        col =0

        worksheet.write(row, col, doc.issn_scielo)
        col += 1

        if 'api' in doc:
            worksheet.write(row, col, doc['collection'])
        col += 1

        worksheet.write(row, col, doc.country)
        col += 1

        worksheet.write(row, col, doc.title)
        col += 1

        worksheet.write(row, col, doc.title_current_status)
        col += 1

        if 'api' in doc:
            if 'first_year' in doc['api']:
                worksheet.write(row, col, int(doc['api']['first_year']))
        col += 1

        worksheet.write(row, col, doc.inclusion_year_at_scielo)
        col += 1

        if 'stopping_year_at_scielo' in doc:
            worksheet.write(row, col, doc.stopping_year_at_scielo)
        col += 1

        worksheet.write(row, col, doc.publisher_name)
        col += 1


        if 'api' in doc:
            if 'url' in doc['api']:
                worksheet.write(row, col, doc.api['url'])
        col += 1

        row += 1

    # Grava planilha Excel
    try:
        workbook.close()
    except IOError as e:
        print(e)
        sys.exit(1)


def main():
    journal_date_list()

if __name__ == "__main__":
    main()