# coding: utf-8
import sys
import xlsxwriter

from reports import headers
import models


def jcatalog():
    # Cria a pasta Excel e adiciona uma planilha
    workbook = xlsxwriter.Workbook('output/journals_catalog.xlsx')
    worksheet = workbook.add_worksheet('SciELO Journals Catalog')

    format_date = workbook.add_format({'num_format': 'dd/mm/yyyy'})

    # Header
    row = 0
    col = 0

    wrap = workbook.add_format({'text_wrap': True})

    for h in headers.scielo_headers:
        worksheet.write(0, col, h, wrap)
        col += 1

    # Extraction date - get date from SciELO, Scopus and JCR collection
    extraction_date = models.Scielo.objects.first().extraction_date

    row = 1

    for dbcol in (
        models.Scielo.objects.filter(collection='scl'),  # SciELO Brazil
        models.Scopus.objects.filter(
            publishers_country='Brazil',
            is_scielo=0,
            source_type='Journal'),  # Scopus - brazilian journals
        models.Jcr.objects.filter(
            country='Brazil',
            is_scielo=0,
            is_scimago=1,
            is_scopus=0)  # JCR - brazilian journals
                ):

        dbname = dbcol._collection.name

        print(dbname + ' ' + str(row))

        for doc in dbcol:

            col = 0

            worksheet.write(row, col, extraction_date, format_date)
            col += 1

            # SciELO ou Scopus ou WoS
            if doc.is_scielo == 1 or doc.is_scopus == 1 or doc.is_jcr == 1:
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
            if doc.is_scielo == 1 and doc.is_scopus == 1 and doc.is_jcr == 1:
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

            # Submissions
            col = 31
            if dbname == 'scielo':

                if doc.is_submissions == 1:

                    sub = models.Submissions.objects.filter(id=doc.submissions_id)[0]

                    if sub:
                        worksheet.write(row, col, sub['scholarone'])
                        col += 1

                        if sub['ojs_scielo'] == 1 or sub['ojs_outro'] == 1:
                            worksheet.write(row, col, 1)
                        else:
                            worksheet.write(row, col, 0)
                        col += 1

                        worksheet.write(row, col, sub['outro'])
                        col += 1
                else:
                    worksheet.write(row, col, 0)
                    col += 1
                    worksheet.write(row, col, 0)
                    col += 1
                    worksheet.write(row, col, 0)
                    col += 1

            # Google H5 M5
            col = 34

            if hasattr(doc, 'google_scholar_h5_2016'):
                worksheet.write_number(row, col, doc.google_scholar_h5_2016)
            col += 1

            if hasattr(doc, 'google_scholar_m5_2016'):
                worksheet.write_number(row, col, doc.google_scholar_m5_2016)
            col += 1

            # DOAJ
            col = 36
            if dbname == 'scielo':
                doaj = models.Doajapi.objects.filter(scielo_id=str(doc.id))
            else:
                if doc.issn_list:
                    doaj = models.Doajapi.objects.filter(issn_list=doc.issn_list[0])

            if doaj:
                worksheet.write_number(row, col, 1)
                col += 1
                worksheet.write(row, col, doaj[0].results[0]['bibjson']['title'])
                col += 1
            else:
                worksheet.write_number(row, col, 0)
                col += 1
            # print(doc.title)
            # Scopus
            col = 38
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

                for year in range(2014, 2017):
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

            # Scimago
            col = 82
            if doc.is_scimago == 1:
                if dbname == 'scimago':
                    docsmago = doc
                else:
                    docsmago = models.Scimago.objects(id=str(doc.scimago_id))[0]

                    if hasattr(docsmago, 'title'):
                        worksheet.write(row, col, docsmago.title)
                    col += 1

                    for year in range(2014, 2017):
                        if hasattr(docsmago, str(year)):
                            for k in [
                                'sjr',
                                'sjr_best_quartile',
                                'h_index',
                                'total_docs',
                                'total_docs_3years',
                                'total_refs',
                                'total_cites_3years',
                                'citable_docs_3years',
                                'cites_by_doc_2years',
                                'ref_by_doc'
                                    ]:
                                if k in docsmago[str(year)]:
                                    worksheet.write(row, col, docsmago[str(year)][k])
                                col += 1
                        else:
                            col += 10

            # WOS
            col = 113

            if doc.is_wos == 1:
                if dbname == 'wos':
                    docsmago = doc
                else:
                    docwos = models.Jcr.objects(id=str(doc.wos_id))[0]

                    year = 2016

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
