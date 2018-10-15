# coding: utf-8
import sys
import xlsxwriter

from reports import headers_scielo_scopus_wos
import models


def jcatalog():
    # Cria a pasta Excel e adiciona uma planilha
    workbook = xlsxwriter.Workbook('output/jcat_scielo_scopus_wos_v2.xlsx')
    worksheet = workbook.add_worksheet('all')

    format_date = workbook.add_format({'num_format': 'dd/mm/yyyy'})

    # Header
    row = 0
    col = 0

    wrap = workbook.add_format({'text_wrap': True})

    for h in headers_scielo_scopus_wos.scielo_headers:
        worksheet.write(0, col, h, wrap)
        col += 1

    # Extraction date - get date from SciELO, Scopus and JCR collection
    extraction_date = models.Scielo.objects.first().extraction_date

    row = 1

    for dbcol in (
        models.Scielo.objects.filter(
            collection='scl'),  # SciELO Brazil

        models.Scopus.objects.filter(
            country='Brazil',
            is_scielo=0,
            source_type='Journal'),  # Scopus - brazilian journals

        models.Wos.objects.filter(
            country='BRAZIL',
            is_scielo=0,
            is_scopus=0)  # WOS - brazilian journals
    ):

        dbname = dbcol._collection.name

        print(dbname)

        for doc in dbcol:

            col = 0

            worksheet.write(row, col, extraction_date, format_date)
            col += 1

            # Source
            worksheet.write(row, col, dbname)
            col += 1

            # titulo
            worksheet.write(row, col, doc.title)
            col += 1

            # SciELO Publisher
            if dbname == 'scielo':
                if 'publisher_name' in doc:
                    worksheet.write(row, col, doc['publisher_name'])
            col += 1

            # Issn SciELO
            if dbname == 'scielo':
                worksheet.write(row, col, doc.issn_scielo)
            col += 1

            # ISSNs
            issns = ', '.join([i for i in doc.issn_list])
            worksheet.write(row, col, issns)
            col += 1

            # country
            worksheet.write(row, col, doc.country)
            col += 1

            # Calculo manual
            col += 3

            # is SciELO
            worksheet.write(row, col, doc.is_scielo)
            col += 1

            # is Scopus
            worksheet.write(row, col, doc.is_scopus)
            col += 1

            # is WoS ALL
            worksheet.write(row, col, doc.is_wos)
            col += 1

            # Wos ('AHCI-SSCI-SSCI')
            if doc.is_wos == 1:
                if dbname != 'wos':
                    docwos = models.Wos.objects(id=str(doc.wos_id))[0]
                    if any(i in docwos.indexes for i in ['ahci', 'scie', 'ssci']):
                        worksheet.write(row, col, 1)
                    else:
                        worksheet.write(row, col, 0)
                else:
                    if any(i in doc.indexes for i in ['ahci', 'scie', 'ssci']):
                        worksheet.write(row, col, 1)
                    else:
                        worksheet.write(row, col, 0)
            else:
                worksheet.write(row, col, 0)
            col += 1

            # Wos ('ESCI')
            if doc.is_wos == 1:
                if dbname != 'wos':
                    docwos = models.Wos.objects(id=str(doc.wos_id))[0]
                    if 'esci' in docwos.indexes:
                        worksheet.write(row, col, 1)
                    else:
                        worksheet.write(row, col, 0)
                else:
                    if 'esci' in doc.indexes:
                        worksheet.write(row, col, 1)
                    else:
                        worksheet.write(row, col, 0)
            else:
                worksheet.write(row, col, 0)
            col += 1

            # status
            col = 15
            if dbname == 'scielo':
                if doc.title_current_status == 'current':
                    worksheet.write(row, col, 1)
                else:
                    worksheet.write(row, col, 0)
            else:
                worksheet.write(row, col, 0)
            col += 1

            # Thematic Areas SciELO
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

            # WOS
            col = 26
            if doc.is_wos == 1:
                if dbname == 'wos':
                    docwos = doc
                else:
                    docwos = models.Wos.objects(id=str(doc.wos_id))[0]
                for k in ['title',
                          'publisher',
                          'thematic_areas']:
                    if hasattr(docwos, k):
                        if k == 'thematic_areas':
                            worksheet.write(row, col, '; '.join(
                                at for at in docwos[k]))
                        else:
                            worksheet.write(row, col, docwos[k])
                    col += 1

            # Scopus
            col = 29
            if doc.is_scopus == 1:
                if dbname == 'scopus':
                    docscopus = doc
                else:
                    docscopus = models.Scopus.objects(id=str(doc.scopus_id))[0]

                for k in [
                    'title',
                    'publishers_name',
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
