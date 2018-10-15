# coding: utf-8
import sys
import xlsxwriter

from reports import headers_scopus_list
import models


def jcatalog():
    # Cria a pasta Excel e adiciona uma planilha
    workbook = xlsxwriter.Workbook('output/scopus_list_rcfapesp_2017.xlsx')
    worksheet = workbook.add_worksheet('scopus')

    format_date = workbook.add_format({'num_format': 'dd/mm/yyyy'})

    # Header
    row = 0
    col = 0

    wrap = workbook.add_format({'text_wrap': True})

    for h in headers_scopus_list.headers:
        worksheet.write(0, col, h, wrap)
        col += 1

    # Extraction date - get date from SciELO collection
    extraction_date = models.Scielo.objects.first().extraction_date

    row = 1

    for dbcol in (
        # SciELO Brazil
        models.Scielo.objects.filter(collection='scl', is_scopus=1),
        # Scopus - brazilian journals (not SciELO)
        models.Scopus.objects.filter(country='Brazil', is_scielo=0),
        # Scopus - others countries
        models.Scopus.objects.filter(country='China'),
        models.Scopus.objects.filter(country='South Korea'),
        models.Scopus.objects.filter(country='Spain'),
        models.Scopus.objects.filter(country='South Africa'),
        models.Scopus.objects.filter(country='India'),
        models.Scopus.objects.filter(country='Russia'),
        models.Scopus.objects.filter(country='Russian Federation'),
        models.Scopus.objects.filter(country='Mexico')
    ):

        dbname = dbcol._collection.name

        print(dbname + ' ' + str(row))

        for doc in dbcol:

            # print(str(doc.issn_list))

            col = 0

            worksheet.write(row, col, extraction_date, format_date)
            col += 1

            # is SciELO
            worksheet.write(row, col, doc.is_scielo)
            col += 1

            # is Scopus
            worksheet.write(row, col, doc.is_scopus)
            col += 1

            # titulo
            col = 3
            worksheet.write(row, col, doc.title)
            col += 1

            # Issn SciELO
            if dbname == 'scielo':
                worksheet.write(row, col, doc.issn_scielo)
                col += 1
            else:
                col += 1

            # ISSNs
            col = 5
            issns = []
            for i in doc.issn_list:
                if issns:
                    issns = issns + ',' + i
                else:
                    issns = i
            if issns:
                worksheet.write(row, col, issns)
            col += 1

            # status
            if dbname == 'scielo':

                if doc.title_current_status == 'current':
                    worksheet.write(row, col, 1)
                else:
                    worksheet.write(row, col, 0)
            col += 1

            # country
            if 'country' in doc:
                worksheet.write(row, col, doc.country)
            col += 1

            # Scopus
            col = 8
            if doc.is_scopus == 1:

                if dbname == 'scopus':
                    docscopus = doc
                else:
                    docscopus = models.Scopus.objects(id=str(doc.scopus_id))[0]

                year = 2017

                if hasattr(docscopus, str(year)):

                    for k in [
                        'citescore',
                        'sjr',
                        'snip'
                    ]:

                        if k in docscopus[str(year)]:
                            worksheet.write(row, col, docscopus[str(year)][k])
                        col += 1
                else:
                    col += 3

                if 'sourcerecord_id' in docscopus:
                    url = 'https://www.scopus.com/sourceid/' + \
                        str(docscopus['sourcerecord_id'])
                    worksheet.write(row, col, url)

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
