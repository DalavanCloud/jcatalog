# coding: utf-8
import sys
import xlsxwriter

import models


def jcatalog():
    # Cria a pasta Excel e adiciona uma planilha
    workbook = xlsxwriter.Workbook('output/pde_not_respond.xlsx')
    worksheet = workbook.add_worksheet()

    # format_date = workbook.add_format({'num_format': 'dd/mm/yyyy'})

    # Header
    row = 0
    col = 0

    wrap = workbook.add_format({'text_wrap': True})

    headers = ['issn',
               'title',
               'indexado WoS',
               'citações SciELO no SciELO CI/WoS 2017',
               'citações WoS ALL Databases no SciELO CI/WoS 2017',
               'Indexado JCR',
               'Fator de Impacto JCR 2017',
               'indexado Scopus',
               'CiteScore 2017',
               'Google H5 2017',
               'Google M5 2017']

    for h in headers:
        worksheet.write(0, col, h, wrap)
        col += 1

    # Extraction date - get date from SciELO collection
    # extraction_date = models.Scielo.objects.first().extraction_date

    row = 1

    with open('data/scielo/pde/issns_nao_responderam.txt') as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end
    # of each line
    issns = [x.strip() for x in content]

    for i in issns:

        doc = models.Scielofapesp.objects.filter(issn_scielo=i)[0]
        print(str(doc.issn_list))

        col = 0

        # Issn SciELO
        worksheet.write(row, col, doc.issn_scielo)
        col += 1

        # titulo
        worksheet.write(row, col, doc.title)
        col += 1

        # --- indexação WoS, 0, 1
        worksheet.write(row, col, doc.is_wos)
        col += 1

        # --- citações SciELO no SciELO CI/WoS
        worksheet.write(row, col, doc['scieloci']['scieloci_cited_2017'] or 0)
        col += 1

        # --- citações WoS ALL Databases no SciELO CI/WoS
        worksheet.write(row, col, doc['scieloci'][
                        'scieloci_wos_cited_2017'] or 0)
        col += 1

        # --- indexação JCR, 0,1
        worksheet.write(row, col, doc.is_jcr)
        col += 1

        # --- Fator de Impacto JCR
        if doc.is_jcr == 1:
            docjcr = models.Jcr.objects(id=str(doc.jcr_id))[0]
            year = 2017
            if hasattr(docjcr, str(year)):
                if 'journal_impact_factor' in docjcr[str(year)]:
                    worksheet.write(row, col, docjcr[str(year)][
                                    'journal_impact_factor'])
        col += 1

        # --- Indexação Scopus, 0,1
        worksheet.write(row, col, doc.is_scopus)
        col += 1

        # --- CiteScore
        if doc.is_scopus == 1:
            docscopus = models.Scopus.objects(id=str(doc.scopus_id))[0]
            year = 2017
            if hasattr(docscopus, str(year)):
                if 'citescore' in docscopus[str(year)]:
                    worksheet.write(row, col, docscopus[
                                    str(year)]['citescore'])
        col += 1

        ndoc = models.Scielo.objects.filter(issn_scielo=i)[0]
        # Google H5 M5
        if 'google_scholar_h5_2017' in ndoc:
            worksheet.write(row, col, ndoc['google_scholar_h5_2017'])
        col += 1

        if 'google_scholar_m5_2017' in ndoc:
            worksheet.write(row, col, ndoc['google_scholar_m5_2017'])
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
