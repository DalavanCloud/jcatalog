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

workbook = xlsxwriter.Workbook('output/scopus_list_20180403_check.xlsx')
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
    'Main Title (SciELO, Scopus, JCR or WOS)',
    'OECD major categories',
    'OECD minor categories',
    'Scimago Region',
    'Scopus Country',
    'SciELO Country',
    'JCR country',
    'is Scopus',
    'is SciELO',
    'is JCR',
    'is WOS',
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
for y in range(2016, 2010, -1):
    worksheet.write(0, col, 'Scopus CiteScore ' + str(y), wrap_blue)
    col += 1

# CWTS SNIP 2016-1999
for y in range(2016, 1998, -1):
    worksheet.write(0, col, 'CWTS SNIP ' + str(y), wrap)
    col += 1

# Scimago fields
worksheet.write(0, col, 'Scimago Title', wrap_orange)
col += 1

# Scimago Indicators 2016-1999
for y in range(2016, 1998, -1):
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
for y in range(2016, 2011, -1):
    for h in [
        'SciELO Total Docs',
        'SciELO Citable Docs'
            ]:
        worksheet.write(0, col, h + ' ' + str(y), wrap_red)
        col += 1

# JCR CIs and Thematic Areas
for h in [
    'JCR SCIE',
    'JCR SSCI',
    'JCR Title',
    'JCR Publisher',
    'JCR Thematic Areas'
        ]:

    worksheet.write(0, col, h, wrap_green)
    col += 1

# JCR Indicators 2016-1997
for y in range(2016, 1996, -1):
    for h in [
        'JCR Total cites',
        'JCR Journal Impact Factor',
        'JCR Impact Factor without Journal Self Cites',
        'JCR 5 years Impact Factor',
        'JCR Immediacy Index',
        'JCR Citable Items',
        'JCR Cited half life',
        'JCR Citing half life',
        'JCR Eigenfactor Score',
        'JCR Article Influence Score',
        'JCR % Articles in Citable Items',
        'JCR Average Journal Impact Factor Percentile',
        'JCR Normalized Eigenfactor'
            ]:

        worksheet.write(0, col, h + ' ' + str(y), wrap_green)
        col += 1

row = 1

# SCOPUS
scopus = models.Scopus.objects()

for docscopus in scopus:
    print('Scopus : ' + docscopus.title)

    col = 0

    if hasattr(docscopus, 'issn_list'):
        worksheet.write(row, col, '; '.join(docscopus.issn_list))
    col += 1

    if docscopus.is_scielo == 1:
        query = models.Scielo.objects.filter(id=str(docscopus.scielo_id))
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

    col = 4
    if docscopus.is_scielo == 1:
        query = models.Scielo.objects.filter(id=str(docscopus.scielo_id))
        worksheet.write(row, col, query[0]['region'])
    else:
        if docscopus.is_scimago == 1:
            query = models.Scimago.objects.filter(id=str(docscopus.scimago_id))
            worksheet.write(row, col, query[0]['region'])
    col += 1

    if hasattr(docscopus, 'publishers_country'):
        worksheet.write(row, col, docscopus.publishers_country)
    col += 1

    if hasattr(docscopus, 'country_scielo'):
        worksheet.write(row, col, docscopus.country_scielo)
    col += 1

    if hasattr(docscopus, 'country_jcr'):
        worksheet.write(row, col, docscopus.country_jcr)
    col += 1

    if hasattr(docscopus, 'is_scopus'):
        worksheet.write(row, col, docscopus.is_scopus)
    col += 1

    if hasattr(docscopus, 'is_scielo'):
        worksheet.write(row, col, docscopus.is_scielo)
    col += 1

    if hasattr(docscopus, 'is_jcr'):
        worksheet.write(row, col, docscopus.is_jcr)
    col += 1

    if hasattr(docscopus, 'is_wos'):
        worksheet.write(row, col, docscopus.is_wos)
    col += 1

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

    col = 17
    for year in range(2016, 2010, -1):
        if hasattr(docscopus, str(year)):
            # print(docscopus[str(year)])
            if 'citescore' in docscopus[str(year)]:
                worksheet.write(row, col, docscopus[str(year)]['citescore'])
        col += 1

    # CWTS SNIP
    col = 23
    if docscopus.is_cwts == 1:
        cwts = models.Cwts.objects(id=str(docscopus.cwts_id))[0]
        for year in range(2016, 1998, -1):
            if hasattr(cwts, str(year)):
                if 'snip' in cwts[str(year)]:
                    worksheet.write(row, col, round(cwts[str(year)]['snip'], 3))
            col += 1

    # SCIMAGO indicators
    col = 41
    if docscopus.is_scimago == 1:

        scimago = models.Scimago.objects(id=str(docscopus.scimago_id))[0]

        if hasattr(scimago, 'title'):
            worksheet.write(row, col, scimago['title'])
        col += 1

        for year in range(2016, 1998, -1):
            if hasattr(scimago, str(year)):
                if 'sjr' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['sjr'])
                col += 1

                if 'sjr_best_quartile' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['sjr_best_quartile'])
                col += 1

                if 'h_index' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['h_index'])
                col += 1

                if 'total_docs' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['total_docs'])
                col += 1

                if 'total_docs_3years' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['total_docs_3years'])
                col += 1

                if 'total_refs' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['total_refs'])
                col += 1

                if 'total_cites_3years' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['total_cites_3years'])
                col += 1


                if 'citable_docs_3years' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['citable_docs_3years'])
                col += 1

                if 'cites_by_doc_2years' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['cites_by_doc_2years'])
                col += 1

                if 'ref_by_doc' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['ref_by_doc'])
                col += 1

            else:
                col += 10

    # SciELO - subjects
    col = 222
    if docscopus.is_scielo == 1:

        scielo = models.Scielo.objects(id=str(docscopus.scielo_id))[0]

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

        for year in range(2016, 2011, -1):

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

    # JCR Indicators 2016-1997
    col = 244
    if docscopus.is_jcr == 1:

        jcr = models.Jcr.objects(id=str(docscopus.jcr_id))[0]

        if hasattr(jcr, 'citation_database'):
            if 'SCIE' in jcr['citation_database']:
                worksheet.write(row, col, 1)
            else:
                worksheet.write(row, col, 0)
            col += 1
            if 'SSCI' in jcr['citation_database']:
                worksheet.write(row, col, 1)
            else:
                worksheet.write(row, col, 0)
            col += 1
        else:
            col += 2

        col = 246
        worksheet.write(row, col, jcr['title'])
        col += 1

        if hasattr(jcr, 'publisher'):
            worksheet.write(row, col, jcr['publisher'])
        col += 1

        col = 248
        if docscopus.is_scielo == 1:
            scielo = models.Scielo.objects(id=str(docscopus.scielo_id))[0]
            if hasattr(scielo, 'thematic_areas'):
                worksheet.write(row, col, '; '.join(scielo['thematic_areas']))
            else:
                if hasattr(jcr, 'thematic_areas'):
                    worksheet.write(row, col, '; '.join(jcr['thematic_areas']))

        col = 249
        for year in range(2016, 1996, -1):
            if hasattr(jcr, str(year)):
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
                    if k in jcr[str(year)]:
                        worksheet.write(
                            row,
                            col,
                            formatindicator(jcr[str(year)][k])
                        )
                    col += 1

    # Avançar linha - prox. documento
    row += 1

print('last line of Scopus: %s' % row)

# -----------------------
# SciELO - is_scopus = 0
scielo = models.Scielo.objects.filter(is_scopus=0)

for doc in scielo:
    print('SciELO : ' + doc.title)

    col = 0

    if hasattr(doc, 'issn_list'):
        worksheet.write(row, col, '; '.join(doc.issn_list))
    col += 1

    if hasattr(doc, 'title'):
        worksheet.write(row, col, doc.title)
    col += 1

    # OECD categories
    col = 2
    if hasattr(doc, 'oecd'):
        loecd = sorted(doc.oecd, key=lambda k: k['code'])
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

    col = 4
    if hasattr(doc, 'region'):
        worksheet.write(row, col, doc.region)
    col += 1

    # Scopus country
    col += 1

    if hasattr(doc, 'country'):
        worksheet.write(row, col, doc.country)
    col += 1

    if hasattr(doc, 'country_jcr'):
        worksheet.write(row, col, doc.country_jcr)
    col += 1

    if hasattr(doc, 'is_scopus'):
        worksheet.write(row, col, doc.is_scopus)
    col += 1

    if hasattr(doc, 'is_scielo'):
        worksheet.write(row, col, doc.is_scielo)
    col += 1

    if hasattr(doc, 'is_jcr'):
        worksheet.write(row, col, doc.is_jcr)
    col += 1

    if hasattr(doc, 'is_wos'):
        worksheet.write(row, col, doc.is_wos)
    col += 1


    # CWTS SNIP
    col = 23
    if doc.is_cwts == 1:
        cwts = models.Cwts.objects(id=str(doc.cwts_id))[0]
        for year in range(2016, 1998, -1):
            if hasattr(cwts, str(year)):
                if 'snip' in cwts[str(year)]:
                    worksheet.write(row, col, round(cwts[str(year)]['snip'], 3))
            col += 1

    # SCIMAGO indicators
    col = 41
    if doc.is_scimago == 1:

        scimago = models.Scimago.objects(id=str(doc.scimago_id))[0]

        worksheet.write(row, col, scimago['title'])
        col += 1

        for year in range(2016, 1998, -1):

            if hasattr(scimago, str(year)):
                if 'sjr' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['sjr'])
                col += 1

                if 'sjr_best_quartile' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['sjr_best_quartile'])
                col += 1

                if 'h_index' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['h_index'])
                col += 1

                if 'total_docs' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['total_docs'])
                col += 1

                if 'total_docs_3years' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['total_docs_3years'])
                col += 1

                if 'total_refs' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['total_refs'])
                col += 1

                if 'total_cites_3years' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['total_cites_3years'])
                col += 1


                if 'citable_docs_3years' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['citable_docs_3years'])
                col += 1

                if 'cites_by_doc_2years' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['cites_by_doc_2years'])
                col += 1

                if 'ref_by_doc' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['ref_by_doc'])
                col += 1

            else:
                col += 10

    # SciELO - subjects
    col = 222

    worksheet.write(row, col, doc['title'])
    col += 1

    if hasattr(doc, 'publisher_name'):
        worksheet.write(row, col, doc.publisher_name)
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
        if doc[k]:
            worksheet.write(row, col, doc[k])
        else:
            worksheet.write(row, col, 0)

        col += 1

    for year in range(2016, 2011, -1):

        k = 'documents_at_' + str(year)
        if hasattr(doc, k):
            worksheet.write(row, col, doc[k])
        col += 1

        k = 'citable_documents_at_' + str(year)
        if hasattr(doc, k):
            worksheet.write(row, col, doc[k])
        col += 1
    else:
        col += 2

    # JCR Indicators 2016-1997
    col = 244
    if doc.is_jcr == 1:

        jcr = models.Jcr.objects(id=str(doc.jcr_id))[0]

        if hasattr(jcr, 'citation_database'):
            if 'SCIE' in jcr['citation_database']:
                worksheet.write(row, col, 1)
            else:
                worksheet.write(row, col, 0)
            col += 1
            if 'SSCI' in jcr['citation_database']:
                worksheet.write(row, col, 1)
            else:
                worksheet.write(row, col, 0)
            col += 1
        else:
            col += 2

        col = 246
        worksheet.write(row, col, jcr['title'])
        col += 1

        if hasattr(jcr, 'publisher'):
            worksheet.write(row, col, jcr['publisher'])
        col += 1

        col = 248
        if hasattr(jcr, 'thematic_areas'):
            worksheet.write(row, col, '; '.join(jcr['thematic_areas']))

        col = 249
        for year in range(2016, 1996, -1):
            if hasattr(jcr, str(year)):
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
                    if k in jcr[str(year)]:
                        worksheet.write(
                            row,
                            col,
                            formatindicator(jcr[str(year)][k])
                        )
                    col += 1

    # Avançar linha - prox. documento
    row += 1

print('last line of SciELO: %s' % row)

# --------------------------------
# JCR - is_scopus=0, is_scielo = 0
jcr = models.Jcr.objects.filter(is_scopus=0, is_scielo=0)

for doc in jcr:
    print('JCR: ' + doc.title)

    col = 0

    if hasattr(doc, 'issn_list'):
        worksheet.write(row, col, '; '.join(doc.issn_list))
    col += 1

    if hasattr(doc, 'title'):
        worksheet.write(row, col, doc.title)
    col += 1

    # OECD categories
    col = 2
    if hasattr(doc, 'oecd'):
        loecd = sorted(doc.oecd, key=lambda k: k['code'])
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

    col = 4
    if doc.is_scimago == 1:
        query = models.Scimago.objects.filter(id=str(doc.scimago_id))
        worksheet.write(row, col, query[0]['region'])
    col += 1

    # Scopus country
    col += 1

    # SciELO country
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

    if hasattr(doc, 'is_jcr'):
        worksheet.write(row, col, doc.is_jcr)
    col += 1

    # open access
    col += 1

    # CWTS SNIP
    # col = 22
    # if doc.is_cwts == 1:
    #     cwts = models.Cwts.objects(id=str(doc.cwts_id))[0]
    #     for year in range(2016, 1998, -1):
    #         if hasattr(cwts, str(year)):
    #             if 'snip' in cwts[str(year)]:
    #                 worksheet.write(row, col, round(cwts[str(year)]['snip'], 3))
    #         col += 1

    # SCIMAGO indicators
    col = 41
    if doc.is_scimago == 1:

        scimago = models.Scimago.objects(id=str(doc.scimago_id))[0]

        worksheet.write(row, col, scimago['title'])
        col += 1

        for year in range(2016, 1998, -1):

            if hasattr(scimago, str(year)):
                if 'sjr' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['sjr'])
                col += 1

                if 'sjr_best_quartile' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['sjr_best_quartile'])
                col += 1

                if 'h_index' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['h_index'])
                col += 1

                if 'total_docs' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['total_docs'])
                col += 1

                if 'total_docs_3years' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['total_docs_3years'])
                col += 1

                if 'total_refs' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['total_refs'])
                col += 1

                if 'total_cites_3years' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['total_cites_3years'])
                col += 1


                if 'citable_docs_3years' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['citable_docs_3years'])
                col += 1

                if 'cites_by_doc_2years' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['cites_by_doc_2years'])
                col += 1

                if 'ref_by_doc' in scimago[str(year)]:
                    worksheet.write(row, col, scimago[str(year)]['ref_by_doc'])
                col += 1

            else:
                col += 10

    # JCR Indicators 2016-1997
    col = 244
    if hasattr(doc, 'citation_database'):
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
    else:
        col += 2

    col = 246
    if hasattr(doc, 'title'):
        worksheet.write(row, col, doc.title)
    col += 1
    if hasattr(doc, 'publisher'):
        worksheet.write(row, col, doc.publisher)
    col += 1

    col = 248
    if hasattr(doc, 'thematic_areas'):
        worksheet.write(row, col, '; '.join(doc['thematic_areas']))

    col = 249
    for year in range(2016, 1996, -1):
        if hasattr(doc, str(year)):
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
                if k in doc[str(year)]:
                    worksheet.write(
                        row,
                        col,
                        formatindicator(doc[str(year)][k])
                    )
                col += 1

    # Avançar linha - prox. documento
    row += 1

print('last line of JCR: %s' % row)

# Grava planilha Excel
workbook.close()
