# coding: utf-8
import sys
import xlsxwriter

import models


def jcatalog():
    # Cria a pasta Excel e adiciona uma planilha
    workbook = xlsxwriter.Workbook('output/check_dates.xlsx')
    worksheet = workbook.add_worksheet()

    # format_date = workbook.add_format({'num_format': 'dd/mm/yyyy'})

    # Header
    row = 0
    col = 0

    wrap = workbook.add_format({'text_wrap': True})

    headers = ['collection',
               'issn_scielo',
               'title',
               'startDate',
               'endDate']

    for h in headers:
        worksheet.write(0, col, h, wrap)
        col += 1

    row = 1
    issns = models.Issnorg.objects()
    for j in issns:

        scielo = models.Scielo.objects.filter(issn_scielo=j.issn_scielo)

        if scielo:

            col = 0

            # Collection
            worksheet.write(row, col, j.collection)
            col += 1

            # Issn SciELO
            worksheet.write(row, col, j.issn_scielo)
            col += 1

            # title
            worksheet.write(row, col, j.title)
            col += 1

            print(j['issn_scielo'])
            # Dates at ISSN.ORG
            for d in j['@graph']:
                for k in list(d.keys()):
                    if k == 'startDate':
                        col = 3
                        worksheet.write(row, col, d['startDate'])
                    if k == 'endDate':
                        col = 4
                        worksheet.write(row, col, d['endDate'])

            # Avançar linha - prox. documento
            row += 1

    # Grava planilha Excel
    try:
        workbook.close()
    except IOError as e:
        print(e)
        sys.exit(1)


def main():
    jcatalog()

if __name__ == "__main__":
    main()
