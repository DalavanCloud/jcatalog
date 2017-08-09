# coding: utf-8
import xlsxwriter
import models

# Cria a pasta Excel e adiciona uma planilha.
workbook = xlsxwriter.Workbook('output/scopus_list.xlsx')
worksheet = workbook.add_worksheet('Scopus indicators')

# Header
col = 0
wrap = workbook.add_format({'text_wrap': True})

for h in [
    'ISSNs',
    'Scopus source type',
    'Title Scopus/SciELO/Wos',
    'Scopus country',
    'SciELO country',
    'WoS country',
    'is Scopus',
    'is SciELO',
    'is WoS',
    'SCIE',
    'SSCI',
    # 2016 - Scopus
    'CiteScore 2016',
    'SNIP 2016',
    'SJR 2016',
    'Best Quartile 2016',
    'Cites/Doc(2 years) 2016',
    # 2015
    'CiteScore 2015',
    'SNIP 2015',
    'SJR 2015',
    'Best Quartile 2015',
    'Cites/Doc(2 years) 2015',
    # 2014
    'CiteScore 2014',
    'SNIP 2014',
    'SJR 2014',
    'Best Quartile 2014',
    'Cites/Doc(2 years) 2014',
    # 2013
    'CiteScore 2013',
    'SNIP 2013',
    'SJR 2013',
    'Best Quartile 2013',
    'Cites/Doc(2 years) 2013',
    # 2012
    'CiteScore 2012',
    'SNIP 2012',
    'SJR 2012',
    'Best Quartile 2012',
    'Cites/Doc(2 years) 2012',
    # 2011
    'CiteScore 2011',
    'SNIP 2011',
    'SJR 2011',
    'Best Quartile 2011',
    'Cites/Doc(2 years) 2011',
    # SciELO - subjects
    'SciELO agricultural sciences',
    'SciELO applied social sciences',
    'SciELO biological sciences',
    'SciELO engineering',
    'SciELO exact and earth sciences',
    'SciELO health sciences',
    'SciELO human sciences',
    'SciELO linguistics letters and arts',
    'SciELO multidisciplinary',
    # Scopus - subjects
    'Top level life sciences',
    'Top level social sciences',
    'Top level physical sciences',
    'Top level health sciences',
    '1000 general',
    '1100 agricultural and biological sciences',
    '1200 arts and humanities',
    '1300 biochemistry genetics and molecular biology',
    '1400 business management and accounting',
    '1500 chemical engineering',
    '1600 chemistry',
    '1700 computer science',
    '1800 decision sciences',
    '1900 earth and planetary sciences',
    '2000 economics econometrics and finance',
    '2100 energy',
    '2200 engineering',
    '2300 environmental science',
    '2400 immunology and microbiology',
    '2500 materials science',
    '2600 mathematics',
    '2700 medicine',
    '2800 neuroscience',
    '2900 nursing',
    '3000 pharmacology toxicology and pharmaceutics',
    '3100 physics and astronomy',
    '3200 psychology',
    '3300 social sciences',
    '3400 veterinary',
    '3500 dentistry',
    '3600 health_professions'
        ]:

    worksheet.write(0, col, h, wrap)

    col += 1

row = 1

# Scopus
scopus = models.Scopus.objects

for docscopus in scopus:
    print('Scopus : ' + docscopus.title)

    col = 0

    if hasattr(docscopus, 'issn_list'):
        worksheet.write(row, col, '; '.join(docscopus.issn_list))
    col += 1

    if hasattr(docscopus, 'source_type'):
        worksheet.write(row, col, docscopus.source_type)
    col += 1

    if hasattr(docscopus, 'title'):
        worksheet.write(row, col, docscopus.title)
    col += 1

    if hasattr(docscopus, 'publishers_country'):
        worksheet.write(row, col, docscopus.publishers_country)
    col += 1

    if hasattr(docscopus, 'country_scielo'):
        worksheet.write(row, col, docscopus.country_scielo)
    col += 1

    if hasattr(docscopus, 'country_wos'):
        worksheet.write(row, col, docscopus.country_wos)
    col += 1

    if hasattr(docscopus, 'is_scopus'):
        worksheet.write(row, col, docscopus.is_scopus)
    col += 1

    if hasattr(docscopus, 'is_scielo'):
        worksheet.write(row, col, docscopus.is_scielo)
    col += 1

    if hasattr(docscopus, 'is_wos'):
        worksheet.write(row, col, docscopus.is_wos)
    col += 1

    if docscopus.is_wos == 1:
        wos = models.Wos.objects(id=str(docscopus.wos_id))[0]
        if hasattr(wos, 'citation_database'):
            if 'SCIE' in wos['citation_database']:
                worksheet.write(row, col, 1)
            else:
                worksheet.write(row, col, 0)
            col += 1
            if 'SSCI' in wos['citation_database']:
                worksheet.write(row, col, 1)
            else:
                worksheet.write(row, col, 0)
            col += 1
    else:
        worksheet.write(row, col, 0)
        col += 1
        worksheet.write(row, col, 0)
        col += 1

    col = 11
    for year in range(2016, 2010, -1):
        if hasattr(docscopus, str(year)):
            # print(docscopus[str(year)])
            if 'citescore' in docscopus[str(year)]:
                worksheet.write(row, col, docscopus[str(year)]['citescore'])
        col += 1

        if hasattr(docscopus, str(year)):
            # print(docscopus[str(year)])
            if 'snip' in docscopus[str(year)]:
                worksheet.write(row, col, docscopus[str(year)]['snip'])
        col += 1

        if hasattr(docscopus, str(year)):
            # print(docscopus[str(year)])
            if 'sjr' in docscopus[str(year)]:
                worksheet.write(row, col, docscopus[str(year)]['sjr'])
        col += 1

        # Scimago
        if docscopus.is_scimago == 1:

            scimago = models.Scimago.objects(id=str(docscopus.scimago_id))[0]

            if hasattr(scimago, str(year)):
                if scimago[str(year)]['sjr_best_quartile']:
                    worksheet.write(row, col, scimago[str(year)]['sjr_best_quartile'])
                col += 1

                if scimago[str(year)]['cites_by_doc_2years']:
                    worksheet.write(row, col, scimago[str(year)]['cites_by_doc_2years'])
                col += 1
            else:
                col += 2
        else:
            col += 2

    # SciELO - subjects
    col = 41
    if docscopus.is_scielo == 1:

        scielo_subj = models.Scielo.objects(id=str(docscopus.scielo_id))[0]

        for k in [
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
            if scielo_subj[k]:
                worksheet.write(row, col, scielo_subj[k])
            else:
                worksheet.write(row, col, 0)

            col += 1

    # Scopus - subjects
    col = 50
    for k in [
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

print('last line of Scopus: %s' % row)

# -----------------------
# SciELO - is_scopus = 0
scielo = models.Scielo.objects.filter(is_scopus=0)

for doc in scielo:
    print(doc.title)

    col = 0

    if hasattr(doc, 'issn_list'):
        worksheet.write(row, col, '; '.join(doc.issn_list))
    col += 1

    # if hasattr(docscopus, 'source_type'):
    #     worksheet.write(row, col, docscopus.source_type)
    col += 1

    if hasattr(doc, 'title'):
        worksheet.write(row, col, doc.title)
    col += 1

    # if hasattr(doc, 'publishers_country'):
    #     worksheet.write(row, col, doc.publishers_country)
    col += 1

    if hasattr(doc, 'country'):
        worksheet.write(row, col, doc.country)
    col += 1

    if hasattr(doc, 'country_wos'):
        worksheet.write(row, col, doc.country_wos)
    col += 1

    if hasattr(doc, 'is_scopus'):
        worksheet.write(row, col, doc.is_scopus)
    col += 1

    if hasattr(doc, 'is_scielo'):
        worksheet.write(row, col, doc.is_scielo)
    col += 1

    if hasattr(doc, 'is_wos'):
        worksheet.write(row, col, doc.is_wos)
    col += 1

    if doc.is_wos == 1:
        wos = models.Wos.objects(id=str(doc.wos_id))[0]
        if hasattr(wos, 'citation_database'):
            if 'SCIE' in wos['citation_database']:
                worksheet.write(row, col, 1)
            else:
                worksheet.write(row, col, 0)
            col += 1
            if 'SSCI' in wos['citation_database']:
                worksheet.write(row, col, 1)
            else:
                worksheet.write(row, col, 0)
            col += 1
    else:
        worksheet.write(row, col, 0)
        col += 1
        worksheet.write(row, col, 0)
        col += 1

    # SciELO - subjects
    col = 41
    for k in [
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
        if doc[k]:
            worksheet.write(row, col, doc[k])
        else:
            worksheet.write(row, col, 0)

        col += 1

    # Avançar linha - prox. documento
    row += 1

print('last line of SciELO: %s' % row)

# JCR - is_scopus=0, is_scielo = 0
wos = models.Wos.objects.filter(is_scopus=0, is_scielo=0)

for doc in wos:
    print('WoS: ' + doc.title)

    col = 0

    if hasattr(doc, 'issn_list'):
        worksheet.write(row, col, '; '.join(doc.issn_list))
    col += 1

    # if hasattr(docscopus, 'source_type'):
    #     worksheet.write(row, col, docscopus.source_type)
    col += 1

    if hasattr(doc, 'title'):
        worksheet.write(row, col, doc.title)
    col += 1

    # if hasattr(doc, 'publishers_country'):
    #     worksheet.write(row, col, doc.publishers_country)
    col += 1

    # if hasattr(doc, 'country_scielo'):
    #     worksheet.write(row, col, doc.country_scielo)
    col += 1

    if hasattr(doc, 'country'):
        worksheet.write(row, col, doc.country)
    col += 1

    if hasattr(doc, 'is_scopus'):
        worksheet.write(row, col, doc.is_scopus)
    col += 1

    if hasattr(doc, 'is_scielo'):
        worksheet.write(row, col, doc.is_scielo)
    col += 1

    if hasattr(doc, 'is_wos'):
        worksheet.write(row, col, doc.is_wos)
    col += 1

    if 'SCIE' in doc['citation_database']:
        worksheet.write(row, col, 1)
    else:
        worksheet.write(row, col, 0)
    col += 1
    if 'SSCI' in doc['citation_database']:
        worksheet.write(row, col, 1)
    else:
        worksheet.write(row, col, 0)
    col += 1

    # Avançar linha - prox. documento
    row += 1

# Grava planilha Excel
workbook.close()
