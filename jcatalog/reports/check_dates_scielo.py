# coding: utf-8
import sys
import xlsxwriter

import models


def jcatalog():
    # Cria a pasta Excel e adiciona uma planilha
    workbook = xlsxwriter.Workbook('output/check_dates_scielo.xlsx')
    worksheet = workbook.add_worksheet('import')

    # format_date = workbook.add_format({'num_format': 'dd/mm/yyyy'})

    # Header
    row = 0
    col = 0

    wrap = workbook.add_format({'text_wrap': True})

    headers = ['collection',
               'issn_scielo',
               'title',
               'check_data 1 or 0',
               'journal_creation_date',
               'issnorg_startDate',
               'entrada_scielo']

    for h in headers:
        worksheet.write(0, col, h, wrap)
        col += 1

    row = 1
    scielo = models.Scielo.objects()
    for doc in scielo:
        print(doc.issn_scielo)

        # Obtem a data de issn_org
        issn_start_date = None
        issn = models.Issnorg.objects.filter(issn_scielo=doc.issn_scielo)

        if issn:
            j = issn[0]
            # Dates at ISSN.ORG
            for d in j['@graph']:
                for k in list(d.keys()):
                    if k == 'startDate':
                        if 'u' not in d['startDate']:
                            if '|' not in d['startDate']:
                                issn_start_date = int(d['startDate'])
                            else:
                                issn_start_date = d['startDate']
                        else:
                            issn_start_date = d['startDate']

        col = 0
        # Collection
        worksheet.write(row, col, doc.collection)
        col += 1

        # Issn SciELO
        worksheet.write(row, col, doc.issn_scielo)
        col += 1

        # title
        worksheet.write(row, col, doc.title)
        col += 2

        # journal creation date
        if 'journal_creation_date' in doc:
            worksheet.write(row, col, doc.journal_creation_date)
        elif 'api' in doc and 'first_year' in doc['api']:
            worksheet.write(row, col, int(doc['api']['first_year']))
        else:
            worksheet.write(row, col, issn_start_date)
        col += 1

        # ISSN startDate
        if issn_start_date:
            worksheet.write(row, col, issn_start_date)
        col += 1

        # SciELO inclusion year
        worksheet.write(row, col, doc.inclusion_year_at_scielo)
        col += 1

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
