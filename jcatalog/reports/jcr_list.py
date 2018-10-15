# coding: utf-8
import sys
import xlsxwriter

from reports import headers_jcr_list
import models


def jcatalog():
    # Cria a pasta Excel e adiciona uma planilha
    workbook = xlsxwriter.Workbook('output/jcr_list_2017.xlsx')
    worksheet = workbook.add_worksheet('jcr')

    format_date = workbook.add_format({'num_format': 'dd/mm/yyyy'})

    # Header
    row = 0
    col = 0

    wrap = workbook.add_format({'text_wrap': True})

    for h in headers_jcr_list.headers:
        worksheet.write(0, col, h, wrap)
        col += 1

    # Extraction date - get date from SciELO collection
    extraction_date = models.Scielo.objects.first().extraction_date

    row = 1

    for dbcol in (
        # SciELO Brazil
        models.Scielo.objects.filter(collection='scl', is_jcr=1),
        # JCR - brazilian journals (not SciELO)
        models.Jcr.objects.filter(country='Brazil', is_scielo=0),
        # JCR - others countries
        models.Jcr.objects.filter(country='China'),
        models.Jcr.objects.filter(country='Peoples R China'),
        models.Jcr.objects.filter(country='South Korea'),
        models.Jcr.objects.filter(country='Spain'),
        models.Jcr.objects.filter(country='South Africa'),
        models.Jcr.objects.filter(country='India'),
        models.Jcr.objects.filter(country='Russia'),
        models.Jcr.objects.filter(country='Russian Federation'),
        models.Jcr.objects.filter(country='Mexico')
    ):

        dbname = dbcol._collection.name

        print(dbname + ' ' + str(row))

        for doc in dbcol:

            col = 0

            worksheet.write(row, col, extraction_date, format_date)
            col += 1

            # is SciELO
            worksheet.write(row, col, doc.is_scielo)
            col += 1

            # is JCR
            worksheet.write(row, col, doc.is_jcr)
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

            # JCR
            col = 8
            if doc.is_jcr == 1:

                if dbname == 'jcr':
                    docwos = doc
                else:
                    docwos = models.Jcr.objects(id=str(doc.jcr_id))[0]

                year = 2017

                if hasattr(docwos, str(year)):

                    for k in [
                        'total_cites',
                        'journal_impact_factor',
                        'impact_factor_without_journal_self_cites',
                        'five_year_impact_factor',
                        'immediacy_index',
                        'citable_items',
                        'cited_half_life',
                        'citing_half_life',
                        'eigenfactor_score',
                        'article_influence_score',
                        'percentage_articles_in_citable_items',
                        'average_journal_impact_factor_percentile',
                        'normalized_eigenfactor'
                    ]:

                        if k in docwos[str(year)]:
                            ind = formatindicator(docwos[str(year)][k])
                            worksheet.write(
                                row,
                                col,
                                ind
                            )
                        col += 1
                else:
                    col += 13

            # Avançar linha - prox. documento
            row += 1

    # Grava planilha Excel
    try:
        workbook.close()
    except IOError as e:
        print(e)
        sys.exit(1)


def formatindicator(indicator):

    data = indicator

    if indicator == 0:
        data = '0'

    if type(indicator) == str:
        if indicator == 'Not Available' or '>' in indicator:
            data = str(indicator)
        else:
            data = float(indicator)

    if type(indicator) == float:
        data = indicator

    return data


def main():
    jcatalog()

if __name__ == "__main__":
    main()
