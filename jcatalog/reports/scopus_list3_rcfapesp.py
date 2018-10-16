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
            models.Scielo.objects.filter(is_scopus=1),
            # Scopus - others countries
            models.Scopus.objects.filter(is_scielo=0)):

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

            # publisher name
            col = 4
            if dbname == 'scielo':
                if 'publisher_name' in doc:
                    worksheet.write(row, col, doc.publisher_name)
            else:
                if 'publishers_name' in doc:
                    worksheet.write(row, col, doc.publishers_name)
            col += 1

            # Issn SciELO
            if dbname == 'scielo':
                worksheet.write(row, col, doc.issn_scielo)
            col += 1

            # ISSNs
            col = 6
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
            col = 9
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
                col += 1

            # areas do Scopus
            col = 13
            if doc.is_scopus == 1:
                if dbname == 'scopus':
                    docscopus = doc
                else:
                    docscopus = models.Scopus.objects(id=str(doc.scopus_id))[0]

                for k in [
                    'sourcerecord_id',
                    'active_or_inactive',
                    'all_science_classification_codes_asjc',
                    'coverage',
                    'top_level_life_sciences',
                    'top_level_social_sciences',
                    'top_level_physical_sciences',
                    'top_level_health_sciences',
                    'c1000_general',
                    'c1100_agricultural_and_biological_sciences',
                    'c1200_arts_and_humanities',
                    'c1300_biochemistry_genetics_and_molecular_biology',
                    'c1400_business_management_and_accounting',
                    'c1500_chemical_engineering',
                    'c1600_chemistry',
                    'c1700_computer_science',
                    'c1800_decision_sciences',
                    'c1900_earth_and_planetary_sciences',
                    'c2000_economics_econometrics_and_finance',
                    'c2100_energy',
                    'c2200_engineering',
                    'c2300_environmental_science',
                    'c2400_immunology_and_microbiology',
                    'c2500_materials_science',
                    'c2600_mathematics',
                    'c2700_medicine',
                    'c2800_neuroscience',
                    'c2900_nursing',
                    'c3000_pharmacology_toxicology_and_pharmaceutics',
                    'c3100_physics_and_astronomy',
                    'c3200_psychology',
                    'c3300_social_sciences',
                    'c3400_veterinary',
                    'c3500_dentistry',
                    'c3600_health_professions'
                ]:
                    if hasattr(docscopus, k):
                        worksheet.write(row, col, docscopus[k])
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
