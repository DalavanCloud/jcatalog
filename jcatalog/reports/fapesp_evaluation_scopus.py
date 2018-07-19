# coding: utf-8

import xlsxwriter
import models


def formatindicator(indicator):

    data = indicator

    if indicator == 0:
        data = '0'

    if type(indicator) == str:
        if '.' in indicator and '>' not in indicator:
            data = float(indicator)

    if type(indicator) == float:
        data = indicator

    return data


# Creates the Excel folder and add a worksheet

workbook = xlsxwriter.Workbook('output/scopus_list_20180719.xlsx')
worksheet = workbook.add_worksheet('Scopus_list')


# HEADER

col = 0

wrap = workbook.add_format({'text_wrap': True})
wrap_blue = workbook.add_format({'text_wrap': True, 'bg_color': '#6495ED'})
wrap_red = workbook.add_format({'text_wrap': True, 'bg_color': '#DC143C'})
wrap_orange = workbook.add_format({'text_wrap': True, 'bg_color': '#FFA500'})
wrap_green = workbook.add_format({'text_wrap': True, 'bg_color': '#99FF99'})

for h in [
    'ISSNs',
    'Main Title (Scopus or SciELO)',
    'OECD major categories',
    'OECD minor categories',
    'Scopus Country',
    'SciELO Country',
    'is Scopus',
    'is SciELO',
    'Open Access(Scopus or SciELO)'
]:
    worksheet.write(0, col, h, wrap)
    col += 1

# Scopus fields
for h in [
    'Scopus Title',
    'Scopus Publisher',
    'Scopus source type',
    'Scopus Codes ASJC'
]:
    worksheet.write(0, col, h, wrap_blue)
    col += 1

# Scopus SciteScore 2016-2011
for y in range(2017, 2016, -1):
    worksheet.write(0, col, 'Scopus CiteScore ' + str(y), wrap_blue)
    col += 1

# Scopus SNIP 2016-1999
for y in range(2017, 2016, -1):
    worksheet.write(0, col, 'Scopus SNIP ' + str(y), wrap_blue)
    col += 1

# Scimago fields
worksheet.write(0, col, 'Scimago Title', wrap_orange)
col += 1

# Scimago Indicators 2016-1999
for y in range(2017, 2016, -1):
    for h in [
        'Scimago SJR',
        'Scimago SJR Best Quartile',
        'Scimago H Index',
        'Scimago Total Docs',
        'Scimago Total Docs 3years',
        'Scimago Total Refs',
        'Scimago Total Cites 3years',
        'Scimago Citable Docs 3years',
        'Scimago Cites by Doc(2 years)',
        'Scimago Ref by Doc'
    ]:
        worksheet.write(0, col, h + ' ' + str(y), wrap_orange)
        col += 1

# SciELO fields and Subjects
for h in [
    'SciELO ISSN',
    'SciELO Title',
    'SciELO Publisher',
    'SciELO thematic areas',
    'SciELO agricultural sciences',
    'SciELO applied social sciences',
    'SciELO biological sciences',
    'SciELO engineering',
    'SciELO exact and earth sciences',
    'SciELO health sciences',
    'SciELO human sciences',
    'SciELO linguistics letters and arts',
    'SciELO multidisciplinary'
]:

    worksheet.write(0, col, h, wrap_red)
    col += 1

# SciELO metrics - 2016-2012
for y in range(2017, 2016, -1):
    for h in [
        'SciELO Total Docs',
        'SciELO Citable Docs'
    ]:
        worksheet.write(0, col, h + ' ' + str(y), wrap_red)
        col += 1

row = 1

# SCOPUS
scopus = models.Scopus.objects()
# scopus = models.Scopus.objects.filter(country='Brazil')
for docscopus in scopus:
    print('Scopus : ' + docscopus.title)

    col = 0

    if hasattr(docscopus, 'issn_list'):
        worksheet.write(row, col, '; '.join(docscopus.issn_list))
    col += 1

    if docscopus.is_scielo == 1:
        query = models.Scielofapesp.objects.filter(id=str(docscopus.scielo_id))
        worksheet.write(row, col, query[0]['title'])
    else:
        if hasattr(docscopus, 'title'):
            worksheet.write(row, col, docscopus.title)
    col += 1

    # OECD categories
    col = 2
    if hasattr(docscopus, 'oecd'):
        loecd = sorted(docscopus.oecd, key=lambda k: k['code'])
        major = []
        minor = []
        for d in loecd:
            if '.' not in d['code']:
                major.append(d['code'] + ' ' + d['description'])
            if '.' in d['code']:
                minor.append(d['code'] + ' ' + d['description'])
        worksheet.write(row, col, '; '.join(major))
        col += 1
        worksheet.write(row, col, '; '.join(minor))
        col += 1
    else:
        col += 2

    if hasattr(docscopus, 'publishers_country'):
        worksheet.write(row, col, docscopus.publishers_country)
    col += 1

    if hasattr(docscopus, 'country_scielo'):
        worksheet.write(row, col, docscopus.country_scielo)
    col += 1

    if hasattr(docscopus, 'is_scopus'):
        worksheet.write(row, col, docscopus.is_scopus)
    col += 1

    if hasattr(docscopus, 'is_scielo'):
        worksheet.write(row, col, docscopus.is_scielo)
    col += 1

    # Open Access
    if hasattr(docscopus, 'open_access_status'):
        worksheet.write(row, col, 1)
    elif docscopus.is_scielo == 1:
        worksheet.write(row, col, 1)
    else:
        worksheet.write(row, col, 0)
    col += 1

    # Scopus fields
    if hasattr(docscopus, 'title'):
        worksheet.write(row, col, docscopus.title)
    col += 1

    if hasattr(docscopus, 'publishers_name'):
        worksheet.write(row, col, docscopus.publishers_name)
    col += 1

    if hasattr(docscopus, 'source_type'):
        worksheet.write(row, col, docscopus.source_type)
    col += 1

    if hasattr(docscopus, 'asjc_code_list'):
        worksheet.write(row, col, '; '.join(docscopus['asjc_code_list']))
    col += 1

    col = 13
    for year in range(2017, 2016, -1):
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

    # CWTS SNIP
    # # col = 23
    # if docscopus.is_cwts == 1:
    #     cwts = models.Cwts.objects(id=str(docscopus.cwts_id))[0]
    #     for year in range(2017, 2016, -1):
    #         if hasattr(cwts, str(year)):
    #             if 'snip' in cwts[str(year)]:
    #                 worksheet.write(row, col, round(
    #                     cwts[str(year)]['snip'], 3))
    #         col += 1

    # SCIMAGO indicators
    col = 15
    if docscopus.is_scimago == 1:

        scimago = models.Scimago.objects(id=str(docscopus.scimago_id))[0]

        if hasattr(scimago, 'title'):
            worksheet.write(row, col, scimago['title'])
        col += 1

        for year in range(2017, 2016, -1):
            if hasattr(scimago, str(year)):
                if 'sjr' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['sjr'])
                col += 1

                if 'sjr_best_quartile' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)][
                                    'sjr_best_quartile'])
                col += 1

                if 'h_index' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['h_index'])
                col += 1

                if 'total_docs' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['total_docs'])
                col += 1

                if 'total_docs_3years' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)][
                                    'total_docs_3years'])
                col += 1

                if 'total_refs' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['total_refs'])
                col += 1

                if 'total_cites_3years' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)][
                                    'total_cites_3years'])
                col += 1

                if 'citable_docs_3years' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)][
                                    'citable_docs_3years'])
                col += 1

                if 'cites_by_doc_2years' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)][
                                    'cites_by_doc_2years'])
                col += 1

                if 'ref_by_doc' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['ref_by_doc'])
                col += 1

            else:
                col += 10

    # SciELO - subjects
    col = 26
    if docscopus.is_scielo == 1:

        scielo = models.Scielofapesp.objects(id=str(docscopus.scielo_id))[0]

        worksheet.write(row, col, scielo['issn_scielo'])
        col += 1

        worksheet.write(row, col, scielo['title'])
        col += 1

        worksheet.write(row, col, scielo['publisher_name'])
        col += 1

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
            if scielo[k]:
                worksheet.write(row, col, scielo[k])
            else:
                worksheet.write(row, col, 0)

            col += 1

        for year in range(2017, 2016, -1):
            col = 39

            k = 'documents_at_' + str(year)
            if hasattr(scielo, k):
                worksheet.write(row, col, scielo[k])
            col += 1

            k = 'citable_documents_at_' + str(year)
            if hasattr(scielo, k):
                worksheet.write(row, col, scielo[k])
            col += 1
        else:
            col += 2

    # Avançar linha - prox. documento
    row += 1

print('last line of Scopus: %s' % row)

# Grava planilha Excel
workbook.close()
