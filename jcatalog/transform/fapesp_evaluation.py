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
workbook = xlsxwriter.Workbook('output/fapesp_journals_evaluation.xlsx')
worksheet = workbook.add_worksheet('SciELO Journals')


# HEADER
col = 0

wrap = workbook.add_format({'text_wrap': True})
wrap_blue = workbook.add_format({'text_wrap': True, 'bg_color': '#6495ED'})
wrap_red = workbook.add_format({'text_wrap': True, 'bg_color': '#DC143C'})
wrap_orange = workbook.add_format({'text_wrap': True, 'bg_color': '#FFA500'})
wrap_green = workbook.add_format({'text_wrap': True, 'bg_color': '#99FF99'})

format_date = workbook.add_format({'num_format': 'dd/mm/yyyy'})
format_date_iso = workbook.add_format({'num_format': 'yyyymmdd'})

for h in [
    'extraction_date',
    'issn',
    'issn_todos',
    'titulo_scielo',
    'titulo_scopus',
    'titulo_wos',
    'doi_prefix',
    'doi_publisher',
    'url_scielo',
    'url_journal',
    'publisher_name',
    'pais_scielo',
    'pais_scopus',
    'pais_wos',
    'tipo_instituicao', # avaliacao
    'inst_resp_nivel_1',
    'inst_resp_nivel_2',
    'inst_resp_nivel_3',
    'editor_chefe_1', # avaliacao - revisando
    'lattes_ed_chefe_1',
    'orcid_ed_chefe_1',
    'editor_chefe_2',
    'lattes_editor_chefe_2',
    'orcid_ed_chefe_2',
    'editor_chefe_3',
    'lattes_editor_chefe_3',
    'orcid_ed_chefe_3',
    'scielo_thematic_areas',  # thematic areas scielo
    'scielo_agricultural sciences',
    'scielo_applied social sciences',
    'scielo_biological sciences',
    'scielo_engineering',
    'scielo_exact and earth sciences',
    'scielo_health sciences',
    'scielo_human sciences',
    'scielo_linguistics letters and arts',
    'scielo_multidisciplinary',
    'wos_categories',
    'scielo_status',  # historico
    'data_de_criacao_do_periodico',
    'data_entrada_scielo',
    'data_saida_scielo',
    'data_inicio_colecao_scielo',
    'data_fim_coleção_scielo',
    'cobra_apc',  # APC
    'apc_valor',
    'apc_notas',
    'apc_valores_conceitos',
    'is_scopus',  # indexacao
    'is_wos',
    'is_jcr',
    'is_medline',
    'medline_db_names'
        ]:

    worksheet.write(0, col, h)
    col += 1

# cabecalho numero de documentos
for h in [
    'ate_2007',
    '2008',
    '2009',
    '2010',
    '2011',
    '2012',
    '2013',
    '2014',
    '2015',
    '2016',
    '2017',
    '2018'
        ]:
    worksheet.write(0, col, 'docs_ano_'+h)
    col += 1
    worksheet.write(0, col, 'docs_ing_'+h)
    col += 1
    worksheet.write(0, col, 'docs_por_'+h)
    col += 1
    worksheet.write(0, col, 'docs_esp_'+h)
    col += 1
    worksheet.write(0, col, 'docs_2_mais_idiomas_'+h)
    col += 1
    worksheet.write(0, col, 'docs_outros_idiomas'+h)
    col += 1
    worksheet.write(0, col, 'docs_citable_ano_'+h)  # CITABLES
    col += 1
    worksheet.write(0, col, 'docs_citable_ing_'+h)
    col += 1
    worksheet.write(0, col, 'docs_citable_por_'+h)
    col += 1
    worksheet.write(0, col, 'docs_citable_esp_'+h)
    col += 1
    worksheet.write(0, col, 'docs_citable_2_mais_idiomas_'+h)
    col += 1
    worksheet.write(0, col, 'docs_citable_outros_idiomas_'+h)
    col += 1

# cabecalho Acessos
for ypub in [
    'ate_2011',
    '2012',
    '2013',
    '2014',
    '2015',
    '2016',
    '2017',
    '2018'
        ]:
    for yacc in [
        'ate_2011',
        '2012',
        '2013',
        '2014',
        '2015',
        '2016',
        '2017',
        '2018'
            ]:
        worksheet.write(0, col, 'publicado_'+ypub+'_accesso_'+yacc)
        col += 1

# cabecalho indicadores WoS SciELO CI
for y in range(2008, 2018):
    year = str(y)
    worksheet.write(0, col, 'scieloci_docs_count_'+year)
    col += 1
    worksheet.write(0, col, 'scieloci_cited_'+year)
    col += 1
    worksheet.write(0, col, 'scieloci_wos_cited_'+year)
    col += 1

# cabecalho indicadores Google
for h in [
    '2013',
    '2014',
    '2015',
    '2016',
    '2017'
        ]:
    worksheet.write(0, col, 'google_scholar_h5_'+h)
    col += 1
    worksheet.write(0, col, 'google_scholar_m5_'+h)
    col += 1

# cabecalho indicadores Scopus
for y in [
    '2011',
    '2012',
    '2013',
    '2014',
    '2015',
    '2016'
        ]:
    for i in [
        'citescore',
        'snip',
        'sjr'
           ]:
        worksheet.write(0, col, 'scopus_'+y+'_'+i)
        col += 1

# cabecalho indicadores JCR
for y in [
    '2007',
    '2008',
    '2009',
    '2010',
    '2011',
    '2012',
    '2013',
    '2014',
    '2015',
    '2016'
        ]:
    for i in [
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
        worksheet.write(0, col, 'jcr_'+y+'_'+i)
        col += 1

extraction_date = models.Scielo.objects.first().extraction_date

# SciELO
scielo = models.Scielo.objects.filter(collection='scl')

row = 1

for doc in scielo:
    print(doc.issn_scielo)

    col = 0

    worksheet.write(row, col, extraction_date, format_date_iso)
    col += 1
    worksheet.write(row, col, doc.issn_scielo)
    col += 1
    worksheet.write(row, col, '; '.join(doc.issn_list))
    col += 1
    worksheet.write(row, col, doc.title)
    col += 1

    if doc['is_scopus'] == 1:
        scopus = models.Scopus.objects.filter(id=str(doc.scopus_id))[0]
        worksheet.write(row, col, scopus.title)
    col += 1

    if doc['is_wos'] == 1:
        wos = models.Wos.objects.filter(id=str(doc.wos_id))[0]
        worksheet.write(row, col, wos.title)
    col += 1

    # DOI Prefix e publisher
    worksheet.write(row, col, doc.crossref['doi_provider']['prefix'])
    col += 1
    worksheet.write(row, col, doc.crossref['doi_provider']['publisher'])
    col += 1
    if 'url' in doc['api']:
        worksheet.write(row, col, doc.api['url'])
    col += 1

    # URL
    doajapi = models.Doajapi.objects.filter(issn_list=doc.issn_scielo)
    if doajapi:
        if 'editorial_review' in doajapi[0]['results'][0]['bibjson']:
            url_journal = doajapi[0]['results'][0]['bibjson']['editorial_review']['url']
            worksheet.write(row, col, url_journal)
    col += 1

    worksheet.write(row, col, doc.publisher_name)
    col += 1

    # Country
    worksheet.write(row, col, doc.country)
    col += 1

    if doc['is_scopus'] == 1:
        scopus = models.Scopus.objects.filter(id=str(doc.scopus_id))[0]
        worksheet.write(row, col, scopus.country)
    col += 1

    if doc['is_wos'] == 1:
        wos = models.Wos.objects.filter(id=str(doc.wos_id))[0]
        worksheet.write(row, col, wos.country)
    col += 1

    if 'avaliacao' in doc:
        if 'tipo_inst' in doc['avaliacao']:
            worksheet.write(row, col, doc['avaliacao']['tipo_inst'])
        col += 1
        if 'inst_n1' in doc['avaliacao']:
            worksheet.write(row, col, doc['avaliacao']['inst_n1'])
        col += 1
        if 'inst_n2' in doc['avaliacao']:
            worksheet.write(row, col, doc['avaliacao']['inst_n2'])
        col += 1
        if 'inst_n3' in doc['avaliacao']:
            worksheet.write(row, col, doc['avaliacao']['inst_n3'])
        col += 1

        if 'contatos' in doc['avaliacao']:
            count = 0
            for c in doc['avaliacao']['contatos']:
                name = None; lattes = None; orcid = None
                if c['cargo'] == 'Editor-chefe' or c['cargo'] == 'Editor':
                    count += 1
                    name = c['first_name'] + ' ' + c['last_name']
                    lattes = c['cv_lattes_editor_chefe']
                    orcid = c['orcid_editor_chefe']
                    if name:
                        worksheet.write(row, col, name)
                    col += 1
                    if lattes:
                        worksheet.write(row, col, lattes)
                    col += 1
                    if orcid:
                        worksheet.write(row, col, orcid)
                    col += 1
                if count == 3:
                    break
    else:
        col += 13

    # Thematic Areas
    col = 27
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

    # Historico
    if 'wos_subject_areas' in doc['api']:
        worksheet.write(row, col, '; '.join(doc['api']['wos_subject_areas']))
    col += 1

    worksheet.write(row, col, doc.title_current_status)
    col += 1

    if 'first_year' in doc['api']:
        worksheet.write(row, col, doc['api']['first_year'])
    col += 1

    worksheet.write(row, col, doc.inclusion_year_at_scielo)
    col += 1

    if 'stopping_year_at_scielo' in doc:
        worksheet.write(row, col, doc.stopping_year_at_scielo)
    col += 1

    worksheet.write(row, col, doc.date_of_the_first_document, format_date_iso)
    col += 1

    worksheet.write(row, col, doc.date_of_the_last_document, format_date_iso)
    col += 1

    # APC
    if 'apc' in doc:
        if doc['apc']['apc'] == 'Sim':
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        if doc['apc']['value']:
            worksheet.write(row, col, doc['apc']['value'])
        col += 1

        if doc['apc']['comments']:
            worksheet.write(row, col, doc['apc']['comments'])
        col += 1

        apc_list = []
        for f in range(1, 9):
            coin = None
            value = None
            concept = None
            if 'apc'+str(f)+'_value_coin':
                coin = doc['apc']['apc'+str(f)+'_value_coin']
                value = doc['apc']['apc'+str(f)+'_value']
                concept = doc['apc']['apc'+str(f)+'_concept']
            if coin or value or concept:
                apc_list.append('[%s) value: %s %s - concept: %s]' % (str(f), coin, value, concept))
        if apc_list:
            worksheet.write(row, col, '; '.join(apc_list))
        col += 1
    else:
        worksheet.write(row, col, 0)
        col += 4

    # Indexacao
    worksheet.write(row, col, doc.is_scopus)
    col += 1

    worksheet.write(row, col, doc.is_wos)
    col += 1

    worksheet.write(row, col, doc.is_jcr)
    col += 1

    pubmed = models.Pubmedapi.objects.filter(issn_list=doc.issn_scielo)
    if pubmed:
        worksheet.write(row, col, 1)
        col += 1
        worksheet.write(row, col, '; '.join(pubmed[0]['db_name']))
        col += 1
    else:
        worksheet.write(row, col, 0)
        col += 2

# Documentos
    if 'docs' in doc:
        for h in [
            'anterior',
            '2008',
            '2009',
            '2010',
            '2011',
            '2012',
            '2013',
            '2014',
            '2015',
            '2016',
            '2017',
            '2018'
                ]:
            if 'docs_'+h in doc['docs']:
                worksheet.write(row, col, doc['docs']['docs_'+h] or 0)
            else:
                worksheet.write(row, col, 0)
            col += 1
            if 'document_en_'+h in doc['docs']:
                worksheet.write(row, col, doc['docs']['document_en_'+h] or 0)
            else:
                worksheet.write(row, col, 0)
            col += 1
            if 'document_pt_'+h in doc['docs']:
                worksheet.write(row, col, doc['docs']['document_pt_'+h] or 0)
            else:
                worksheet.write(row, col, 0)
            col += 1
            if 'document_es_'+h in doc['docs']:
                worksheet.write(row, col, doc['docs']['document_es_'+h] or 0)
            else:
                worksheet.write(row, col, 0)
            col += 1
            if 'doc_2_more_lang_'+h in doc['docs']:
                worksheet.write(row, col, doc['docs']['doc_2_more_lang_'+h] or 0)
            else:
                worksheet.write(row, col, 0)
            col += 1
            if 'document_other_languages_'+h in doc['docs']:
                worksheet.write(row, col, doc['docs']['document_other_languages_'+h] or 0)
            else:
                worksheet.write(row, col, 0)
            col += 1
            # CITABLES
            if 'is_citable_'+h in doc['docs']:
                worksheet.write(row, col, doc['docs']['is_citable_'+h] or 0)
            else:
                worksheet.write(row, col, 0)
            col += 1
            if 'citable_en_'+h in doc['docs']:
                worksheet.write(row, col, doc['docs']['citable_en_'+h] or 0)
            else:
                worksheet.write(row, col, 0)
            col += 1
            if 'citable_pt_'+h in doc['docs']:
                worksheet.write(row, col, doc['docs']['citable_pt_'+h] or 0)
            else:
                worksheet.write(row, col, 0)
            col += 1
            if 'citable_es_'+h in doc['docs']:
                worksheet.write(row, col, doc['docs']['citable_es_'+h] or 0)
            else:
                worksheet.write(row, col, 0)
            col += 1
            if 'citable_doc_2_more_lang_'+h in doc['docs']:
                worksheet.write(row, col, doc['docs']['citable_doc_2_more_lang_'+h] or 0)
            else:
                worksheet.write(row, col, 0)
            col += 1
            if 'citable_other_lang_'+h in doc['docs']:
                worksheet.write(row, col, doc['docs']['citable_other_lang_'+h] or 0)
            else:
                worksheet.write(row, col, 0)
            col += 1
# Acessos
    if 'access' in doc:
        for ypub in [
            'anterior',
            '2012',
            '2013',
            '2014',
            '2015',
            '2016',
            '2017',
            '2018'
                ]:
            for yacc in [
                'anterior',
                '2012',
                '2013',
                '2014',
                '2015',
                '2016',
                '2017',
                '2018'
                    ]:
                if 'pub_'+ypub+'_acc_'+yacc in doc['access']:
                    worksheet.write(row, col, doc['access']['pub_'+ypub+'_acc_'+yacc] or 0)
                else:
                    worksheet.write(row, col, 0)
                col += 1
    else:
        col += 64

    # SciELO CI WOS cited
    if 'scieloci' in doc:
        for y in range(2008, 2018):
            year = str(y)
            if 'docs_'+year in doc['scieloci']:
                worksheet.write(row, col, doc['scieloci']['docs_'+year])
            col += 1
            if 'scieloci_'+year in doc['scieloci']:
                worksheet.write(row, col, doc['scieloci']['scieloci_'+year])
            col += 1
            if 'scieloci_wos_'+year in doc['scieloci']:
                worksheet.write(row, col, doc['scieloci']['scieloci_wos_'+year])
            col += 1
    else:
        col += 30

    # Google scholar h5 m5
    for h in [
        '2012',
        '2013',
        '2014',
        '2015',
        '2016'
            ]:
        h2 = int(h)-1
        if 'google_scholar_h5_'+str(h2) in doc:
            worksheet.write(row, col, doc['google_scholar_h5_'+str(h2)])
        col += 1
        if 'google_scholar_m5_'+str(h2) in doc:
            worksheet.write(row, col, doc['google_scholar_m5_'+str(h2)])
        col += 1

    # Scopus
    if doc['is_scopus'] == 1:

        scopus = models.Scopus.objects.filter(id=str(doc.scopus_id))[0]

        for y in [
            '2011',
            '2012',
            '2013',
            '2014',
            '2015',
            '2016'
                ]:
            for i in [
                'citescore',
                'snip',
                'sjr'
                   ]:
                if y in scopus and i in scopus[y]:
                    worksheet.write(row, col, formatindicator(scopus[y][i]))
                col += 1

    # JCR
    if doc['is_jcr'] == 1:

        jcr = models.Jcr.objects.filter(id=str(doc.jcr_id))[0]

        for y in [
            '2007',
            '2008',
            '2009',
            '2010',
            '2011',
            '2012',
            '2013',
            '2014',
            '2015',
            '2016'
                ]:
            for i in [
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
                if y in jcr and i in jcr[y]:
                    worksheet.write(row, col, formatindicator(jcr[y][i]))
                col += 1

    # Avanca linha
    row += 1

# Grava planilha Excel
workbook.close()
