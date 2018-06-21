# coding: utf-8
import sys
import xlsxwriter

from reports import headers_small
import models


def jcatalog():
    # Cria a pasta Excel e adiciona uma planilha
    workbook = xlsxwriter.Workbook('output/journals_scielo_is_scopus.xlsx')
    worksheet = workbook.add_worksheet('SciELO Journals Catalog')

    format_date = workbook.add_format({'num_format': 'dd/mm/yyyy'})

    # Header
    row = 0
    col = 0

    wrap = workbook.add_format({'text_wrap': True})

    for h in headers_small.scielo_headers:
        worksheet.write(0, col, h, wrap)
        col += 1

    # Extraction date - get date from SciELO, Scopus and JCR collection
    extraction_date = models.Scielo.objects.first().extraction_date

    row = 1

    for dbcol in (
        models.Scielo.objects.filter(collection='scl'),  # SciELO Brazil
                ):

        dbname = dbcol._collection.name

        print(dbname + ' ' + str(row))

        for doc in dbcol:

            col = 0

            worksheet.write(row, col, extraction_date, format_date)
            col += 1

            # SciELO ou Scopus ou WoS
            if doc.is_scielo == 1 or doc.is_scopus == 1 or doc.is_wos == 1:
                worksheet.write(row, col, 1)
            else:
                worksheet.write(row, col, 0)
            col += 1

            # is SciELO
            worksheet.write(row, col, doc.is_scielo)
            col += 1

            # is Scopus
            worksheet.write(row, col, doc.is_scopus)
            col += 1

            # is WoS
            worksheet.write(row, col, doc.is_wos)
            col += 1

            # SciELO, Scopus e WoS
            if doc.is_scielo == 1 and doc.is_scopus == 1 and doc.is_wos == 1:
                worksheet.write(row, col, 1)
            else:
                worksheet.write(row, col, 0)
            col += 1

            # SciELO e Scopus
            if doc.is_scielo == 1 and doc.is_scopus == 1:
                worksheet.write(row, col, 1)
            else:
                worksheet.write(row, col, 0)
            col += 1

            # SciELO e WoS
            if doc.is_scielo == 1 and doc.is_wos == 1:
                worksheet.write(row, col, 1)
            else:
                worksheet.write(row, col, 0)
            col += 1

            # Scopus e WoS
            if doc.is_scopus == 1 and doc.is_wos == 1:
                worksheet.write(row, col, 1)
            else:
                worksheet.write(row, col, 0)
            col += 1

            # SciELO ou Scopus
            if doc.is_scielo == 1 or doc.is_scopus == 1:
                worksheet.write(row, col, 1)
            else:
                worksheet.write(row, col, 0)
            col += 1

            # Scopus ou WoS
            if doc.is_scopus == 1 or doc.is_wos == 1:
                worksheet.write(row, col, 1)
            else:
                worksheet.write(row, col, 0)
            col += 1

            # SciELO ou WoS
            if doc.is_scielo == 1 or doc.is_wos == 1:
                worksheet.write(row, col, 1)
            else:
                worksheet.write(row, col, 0)
            col += 1

            # SciELO e (Scopus ou WoS)
            if doc.is_scielo == 1 and (doc.is_scopus == 1 or doc.is_wos == 1):
                worksheet.write(row, col, 1)
            else:
                worksheet.write(row, col, 0)
            col += 1

            # SciELO e não (Scopus)
            if doc.is_scielo == 1 and doc.is_scopus == 0:
                worksheet.write(row, col, 1)
            else:
                worksheet.write(row, col, 0)
            col += 1

            # (Scopus ou WoS) e não SciELO
            if (doc.is_scopus == 1 or doc.is_wos == 1) and doc.is_scielo == 0:
                worksheet.write(row, col, 1)
            else:
                worksheet.write(row, col, 0)
            col += 1

            # titulo
            col = 15
            worksheet.write(row, col, doc.title)
            col += 1

            # ISSNs
            col = 16
            issns = []
            for i in doc.issn_list:
                if issns:
                    issns = issns + ',' + i
                else:
                    issns = i
            if issns:
                worksheet.write(row, col, issns)
            col += 1

            # Issn SciELO
            if dbname == 'scielo':
                worksheet.write(row, col, doc.issn_scielo)
                col += 1
            else:
                col += 1

            # status
            col = 18
            if dbname == 'scielo':

                if doc.title_current_status == 'current':
                    worksheet.write(row, col, 1)
                else:
                    worksheet.write(row, col, 0)
                col += 1

            # Thematic Areas
            for k in [
                'title_thematic_areas',
                'title_is_agricultural_sciences',
                'title_is_applied_social_sciences',
                'title_is_biological_sciences',
                'title_is_engineering',
                'title_is_exact_and_earth_sciences',
                'title_is_health_sciences',
                'title_is_human_sciences',
                'title_is_linguistics_letters_and_arts',
                'title_is_multidisciplinary'
                    ]:
                if k in doc:
                    worksheet.write(row, col, doc[k])
                col += 1

            # Years
            col = 29
            if hasattr(doc, 'inclusion_year_at_scielo'):
                worksheet.write(row, col, doc.inclusion_year_at_scielo)
            else:
                worksheet.write(row, col, '')
            col += 1

            if hasattr(doc, 'stopping_year_at_scielo'):
                worksheet.write(row, col, doc.stopping_year_at_scielo)
            else:
                worksheet.write(row, col, '')
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
