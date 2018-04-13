# coding: utf-8
import xlsxwriter
import models


def formatindicator(indicator):

    data = indicator

    if type(indicator) == str:
        if '.' in indicator and '>' not in indicator:
            data = float(indicator)

    if type(indicator) == float:
        data = indicator

    return data


def timesfmt(data):
    if isinstance(data, float):
        num = round(data, 2)
    elif isinstance(data, int):
        num = data
    else:
        if isinstance(data, str):
            if 'DIV' in data:
                num = 'n/d'
            else:
                num = data
    return num


# Creates the Excel folder and add a worksheet
workbook = xlsxwriter.Workbook('output/fapesp_journals_evaluation_line_r5.xlsx')
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
    'medline_db_names',
    'ano_publicacao', # YEAR
    'num_docs',
    'num_docs_ing',
    'num_docs_por',
    'num_docs_esp',
    'num_docs_2_mais_idiomas',
    'num_docs_outros_idiomas',
    'num_docs_citaveis',
    'num_docs_citaveis_ing',
    'num_docs_citaveis_por',
    'num_docs_citaveis_esp',
    'num_docs_citaveis_2_mais_idiomas',
    'num_docs_citaveis_outros_idiomas'
        ]:

    worksheet.write(0, col, h)
    col += 1

# cabecalho Acessos
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
    worksheet.write(0, col, 'accesso_'+yacc)
    col += 1

# cabecalho SciELO CI; Google Scholar, Scopus; JCR
for h in [
    'scieloci_docs_count',
    'scieloci_cited',
    'scieloci_wos_cited',
    'google_scholar_h5',
    'google_scholar_m5',
    'scopus_citescore',
    'scopus_snip',
    'scopus_sjr',
    'scimago_total_cites_3years',
    'scimago_cites_by_doc_2years',
    'scimago_h_index',
    'jcr_total_cites',
    'jcr_journal_impact_factor',
    'jcr_impact_factor_without_journal_self_cites',
    'jcr_five_year_impact_factor',
    'jcr_immediacy_index',
    'jcr_citable_items',
    'jcr_cited_half_life',
    'jcr_citing_half_life',
    'jcr_eigenfactor_score',
    'jcr_article_influence_score',
    'jcr_percentage_articles_in_citable_items',
    'jcr_average_journal_impact_factor_percentile',
    'jcr_normalized_eigenfactor'
        ]:
    worksheet.write(0, col, h)
    col += 1

# cabecalho Affiliations
for h in [
    'afiliacao_br',
    'afiliacao_estrang',
    'afiliacao_nao_ident',
    'afiliacao_br_estrang',
    'afiliacao_nao_ident_todos'
        ]:
    worksheet.write(0, col, h)
    col += 1

# cabecalho manuscritos
for h in [
    'manuscritos_recebidos_1sem',
    'manuscritos_aprovados_1sem',
    'manuscritos_recebidos_2sem',
    'manuscritos_aprovados_2sem',
    'manuscritos_recebidos_ano',
    'manuscritos_aprovados_ano',
        ]:
    worksheet.write(0, col, h)
    col += 1

# cabecalho tempos entre submissao, aprovacao e publicacao
for h in [
    'media_meses_submissao_aprovacao',
    'desvp_meses_submissao_aprovacao',
    'media_meses_aprovacao_pub_ahp',
    'desvp_meses_aprovacao_pub_ahp',
    'media_meses_aprovacao_pub_scielo',
    'desvp_meses_aprovacao_pub_scielo'
        ]:
    worksheet.write(0, col, h)
    col += 1
extraction_date = models.Scielo.objects.first().extraction_date

# SciELO
scielo = models.Scielo.objects.filter(collection='scl')

row = 1

for doc in scielo:
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
        print(doc.issn_scielo+'_'+str(h))

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

        # ANO DE PUBLICACAO
        if h == 'anterior':
            year = 'ate_2007'
        else:
            year = h
        worksheet.write(row, col, str(year))
        col += 1

        # Documentos
        if 'docs' in doc:
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
        col = 66
        if 'access' in doc:
            if h == 'anterior':
                pass
            elif h == '2011':
                hy = 'anterior'
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
                    if 'pub_'+hy+'_acc_anterior' in doc['access']:
                        worksheet.write(row, col, doc['access']['pub_'+hy+'_acc_'+yacc])
                    else:
                        worksheet.write(row, col, 0)
                    col += 1
            elif int(h) > 2011:
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
                    if 'pub_'+h+'_acc_'+yacc in doc['access']:
                        worksheet.write(row, col, doc['access']['pub_'+h+'_acc_'+yacc] or 0)
                    else:
                        worksheet.write(row, col, 0)
                    col += 1
        else:
            col += 8

        # SciELO CI WOS cited
        col = 74
        if 'scieloci' in doc:
            if h == 'anterior':
                pass
            else:
                year = str(h)

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
            col += 3

        # Google
        col = 77
        if h == 'anterior':
            pass
        else:
            h2 = int(h)-1
            if 'google_scholar_h5_'+str(h2) in doc:
                worksheet.write(row, col, doc['google_scholar_h5_'+str(h2)])
            col += 1
            if 'google_scholar_m5_'+str(h2) in doc:
                worksheet.write(row, col, doc['google_scholar_m5_'+str(h2)])
            col += 1

        # SCOPUS
        col = 79
        if doc['is_scopus'] == 1:
            for i in [
                'citescore',
                'snip',
                'sjr'
                   ]:
                if h in scopus and i in scopus[h]:
                    worksheet.write(row, col, formatindicator(scopus[h][i]))
                col += 1

        # SCIMAGO
        col = 82
        if doc['is_scimago'] == 1:
            scimago = models.Scimago.objects.filter(id=str(doc.scimago_id))[0]
            for i in [
                'total_cites_3years',
                'cites_by_doc_2years',
                'h_index'
                   ]:
                if h in scimago and i in scimago[h]:
                    worksheet.write(row, col, formatindicator(scimago[h][i]))
                col += 1

        # JCR
        col = 85
        if doc['is_jcr'] == 1:
            jcr = models.Jcr.objects.filter(id=str(doc.jcr_id))[0]
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
                if h in jcr and i in jcr[h]:
                    worksheet.write(row, col, formatindicator(jcr[h][i]))
                col += 1
        else:
            col += 13

        # Affiliations_documents
        col = 98
        if 'aff' in doc:
            if h == 'anterior':
                if 'br_ate_2007' in doc['aff']:
                    worksheet.write(row, col, doc['aff']['br_ate_2007'] or 0)
                col += 1
                if 'estrang_ate_2007' in doc['aff']:
                    worksheet.write(row, col, doc['aff']['estrang_ate_2007'] or 0)
                col += 1
                if 'nao_ident_ate_2007' in doc['aff']:
                    worksheet.write(row, col, doc['aff']['nao_ident_ate_2007'] or 0)
                col += 1
                if 'br_estrang_ate_2007' in doc['aff']:
                    worksheet.write(row, col, doc['aff']['br_estrang_ate_2007'] or 0)
                col += 1
                if 'nao_ident_todos_ate_2007' in doc['aff']:
                    worksheet.write(row, col, doc['aff']['nao_ident_todos_ate_2007'] or 0)
                col += 1

            if 'br_'+h in doc['aff']:
                worksheet.write(row, col, doc['aff']['br_'+h] or 0)
            col += 1

            if 'estrang_'+h in doc['aff']:
                worksheet.write(row, col, doc['aff']['estrang_'+h] or 0)

            col += 1
            if 'nao_ident_'+h in doc['aff']:
                worksheet.write(row, col, doc['aff']['nao_ident_'+h] or 0)
            col += 1

            if 'br_estrang_'+h in doc['aff']:
                worksheet.write(row, col, doc['aff']['br_estrang_'+h] or 0)
            col += 1

            if 'nao_ident_todos_'+h in doc['aff']:
                worksheet.write(row, col, doc['aff']['nao_ident_todos_'+h] or 0)
            col += 1
        else:
            col += 5

        # Manuscritos
        col = 103
        if 'manuscritos' in doc:
            if h == '2014':

                col += 4
                if 'recebidos_2014' in doc['manuscritos']:
                    worksheet.write(row, col, doc['manuscritos']['recebidos_2014'])
                col += 1
                if 'aprovados_2014' in doc['manuscritos']:
                    worksheet.write(row, col, doc['manuscritos']['aprovados_2014'])
                col += 1
            else:
                if 'recebidos_'+h+'_1sem' in doc['manuscritos']:
                    worksheet.write(row, col, doc['manuscritos']['recebidos_'+h+'_1sem'])
                col += 1
                if 'aprovados_'+h+'_1sem' in doc['manuscritos']:
                    worksheet.write(row, col, doc['manuscritos']['aprovados_'+h+'_1sem'])
                col += 1

                if 'recebidos_'+h+'_2sem' in doc['manuscritos']:
                    worksheet.write(row, col, doc['manuscritos']['recebidos_'+h+'_2sem'])
                col += 1
                if 'aprovados_'+h+'_2sem' in doc['manuscritos']:
                    worksheet.write(row, col, doc['manuscritos']['aprovados_'+h+'_2sem'])
                col += 1

        # Tempos entre submissao, aprovacao e publicacao
        col = 109
        if 'times' in doc:
            if h == 'anterior':

                if 'media_meses_sub_aprov_ate_2007' in doc['times']:
                    times = timesfmt(doc['times']['media_meses_sub_aprov_ate_2007'])
                    worksheet.write(row, col, times)
                col += 1

                if 'desvpad_meses_sub_aprov_ate_2007' in doc['times']:
                    times = timesfmt(doc['times']['desvpad_meses_sub_aprov_ate_2007'])
                    worksheet.write(row, col, times)
                col += 1

                if 'media_meses_aprov_pub_ahp_ate_2007' in doc['times']:
                    times = timesfmt(doc['times']['media_meses_aprov_pub_ahp_ate_2007'])
                    worksheet.write(row, col, times)
                col += 1

                if 'desvpad_meses_aprov_pub_ahp_ate_2007' in doc['times']:
                    times = timesfmt(doc['times']['desvpad_meses_aprov_pub_ahp_ate_2007'])
                    worksheet.write(row, col, times)
                col += 1

                if 'media_meses_aprov_pub_scielo_ate_2007' in doc['times']:
                    times = timesfmt(doc['times']['media_meses_aprov_pub_scielo_ate_2007'])
                    worksheet.write(row, col, times)
                col += 1

                if 'desvpad_meses_aprov_pub_scielo_ate_2007' in doc['times']:
                    times = timesfmt(doc['times']['desvpad_meses_aprov_pub_scielo_ate_2007'])
                    worksheet.write(row, col, times)
                col += 1

            else:

                if 'media_meses_sub_aprov_'+h in doc['times']:
                    times = timesfmt(doc['times']['media_meses_sub_aprov_'+h])
                    worksheet.write(row, col, times)
                col += 1

                if 'desvpad_meses_sub_aprov_'+h in doc['times']:
                    times = timesfmt(doc['times']['desvpad_meses_sub_aprov_'+h])
                    worksheet.write(row, col, times)
                col += 1

                if 'media_meses_aprov_pub_ahp_'+h in doc['times']:
                    times = timesfmt(doc['times']['media_meses_aprov_pub_ahp_'+h])
                    worksheet.write(row, col, times)
                col += 1

                if 'desvpad_meses_aprov_pub_ahp_'+h in doc['times']:
                    times = timesfmt(doc['times']['desvpad_meses_aprov_pub_ahp_'+h])
                    worksheet.write(row, col, times)
                col += 1

                if 'media_meses_aprov_pub_scielo_'+h in doc['times']:
                    times = timesfmt(doc['times']['media_meses_aprov_pub_scielo_'+h])
                    worksheet.write(row, col, times)
                col += 1

                if 'desvpad_meses_aprov_pub_scielo_'+h in doc['times']:
                    times = timesfmt(doc['times']['desvpad_meses_aprov_pub_scielo_'+h])
                    worksheet.write(row, col, times)
                col += 1

        # Avança ano
        row += 1

# Avança journal
row += 1

# Grava planilha Excel
workbook.close()
