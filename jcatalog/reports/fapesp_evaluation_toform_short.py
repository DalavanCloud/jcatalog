# coding: utf-8
import xlsxwriter
import models
import datetime


def timesfmt(data):
    if isinstance(data, float):
        num = round(data, 2)
    elif isinstance(data, int):
        num = data
    else:
        if isinstance(data, str):
            num = None
    return num


def journal(query, filename, sheetname):
    # Creates the Excel folder and add a worksheet

    workbook = xlsxwriter.Workbook('output/' + filename)
    worksheet = workbook.add_worksheet(sheetname)

    worksheet.freeze_panes(1, 0)
    worksheet.set_row(0, 50)

    # HEADER
    col = 0

    wrap_header = workbook.add_format({'text_wrap': True, 'size': 9})

    for h in [
        'issn',
        'nome_periodico',  # title
        'instituicao',  # publisher
        'entidade',  # tipo_inst
        'depto1',  # inst_nivel1
        'depto2',  # inst_nivel2
        '3-e01 e 3-f0',
        '3-e02',
        '3-e03',
        # '3-e1',
        # '3-e2',
        # '3-e3',
        # '3-e4',
        # '3-f1',
        # '3-f2',
        # '3-g1',
        # '3-g2',
        # '3-g3',
        # '3-g4',
        '3-h01',
        '3-h02',
        # '3-j0',
        # '3-j1',
        # '3-j2',
        # '3-j3',
        # '4-d',
        # '4-f1',
        # '4-f2',
        # '4-f3',
        # '4-f4'
        'corpo_editorial',
        'jcr_average_journal_impact_factor_percentile',
        'scimago_best_quartile'
    ]:

        worksheet.write(0, col, h, wrap_header)
        col += 1

    # SciELO
    scielo = query

    row = 1

    for doc in scielo:
        print(doc.issn_scielo)

        col = 0

        # ISSN SciELO
        worksheet.write(row, col, doc.issn_scielo)
        col += 1

        # Nome do periodico (title)
        worksheet.write(row, col, doc.title)
        col += 1

        # Instituicao
        worksheet.write(row, col, doc.publisher_name)
        col += 1

        # Entidade e Departamento (nivel 1 e 2) - avaliacao
        tipo_i = {
            '1': 'Sociedade científica, Associação Acadêmica ou Profissional',
            '2': 'Universidade, Instituição Acadêmica, Centro de Estudos/Pesquisa',
            '3': 'Ministérios, Secretarias, Instituto de Pesquisa e Desenvolvimento, Centros de Estudos, Outros',
            '4': 'Editora privada'}

        if 'avaliacao' in doc:
            if 'tipo_inst' in doc['avaliacao']:
                tipo = str(doc['avaliacao']['tipo_inst'])
                worksheet.write(row, col, tipo_i[tipo])
            col += 1
            if 'inst_n2' in doc['avaliacao']:
                instn2 = None
                if doc['avaliacao']['inst_n2'] != "-":
                    instn2 = doc['avaliacao']['inst_n2']
                worksheet.write(row, col, instn2)
            col += 1
            if 'inst_n3' in doc['avaliacao']:
                instn3 = None
                if doc['avaliacao']['inst_n3'] != "-":
                    instn3 = doc['avaliacao']['inst_n3']
                worksheet.write(row, col, instn3)
            col += 1
        else:
            col += 3

        # 3-e01, 3-e02, 3-e03 - 2015
        if 'scieloci' in doc:
            if 'docs_2015'in doc['scieloci']:
                worksheet.write(row, col, doc['scieloci']['docs_2015'])
            col += 1
            if 'scieloci_cited_2015' in doc['scieloci']:
                worksheet.write(row, col, doc['scieloci'][
                                'scieloci_cited_2015'])
            col += 1
            if 'scieloci_wos_cited_2015' in doc['scieloci']:
                worksheet.write(row, col, doc['scieloci'][
                                'scieloci_wos_cited_2015'])
            col += 1
        else:
            col += 3

        # 3-e1 a 4, 3-f1 a 2 - 2015
        # if 'form' in doc:
        #     for criterio in [
        #         '3-e1',
        #         '3-e2',
        #         '3-e3',
        #         '3-e4',
        #         '3-f1',
        #         '3-f2'
        #     ]:
        #         if criterio in doc['form']['2015']:
        #             worksheet.write(row, col, doc['form']['2015'][criterio])
        #         col += 1
        # else:
        #     col += 6

        # 3-g - 2017
        # if 'form' in doc:
        #     for criterio in [
        #         '3-g1',
        #         '3-g2',
        #         '3-g3',
        #         '3-g4'
        #     ]:
        #         if criterio in doc['form']['2017']:
        #             worksheet.write(row, col, doc['form']['2017'][criterio])
        #         col += 1
        # else:
        #     col += 4

        # 3-h
        if 'docs' in doc:
            if 'tipo_review_2017' in doc['docs']:
                worksheet.write(row, col, doc['docs']['tipo_review_2017'] or 0)
            col += 1
            if 'is_citable_2017' in doc['docs']:
                worksheet.write(row, col, doc['docs']['is_citable_2017'] or 0)
            col += 1
        else:
            col += 2

        if 'api' in doc:
            acron = doc['api']['acronym']
            url = 'http://www.scielo.br/revistas/' + acron + '/iedboard.htm'
            worksheet.write(row, col, url)
        col += 1

        if doc['is_jcr'] == 1:
            jcr = models.Jcr.objects.filter(id=str(doc.jcr_id))[0]
            if '2017' in jcr:
                worksheet.write(row, col, jcr['2017'][
                                'average_journal_impact_factor_percentile'])
        col += 1

        if doc['is_scimago'] == 1:
            scimago = models.Scimago.objects.filter(id=str(doc.scimago_id))[0]
            if '2017' in scimago:
                worksheet.write(row, col, scimago['2017']['sjr_best_quartile'])

        col += 1
        # 3-j, 4-d, 4-f1 a 2
        # if 'form' in doc:
        #     for criterio in [
        #         '3-j0',
        #         '3-j1',
        #         '3-j2',
        #         '3-j3',
        #         '4-d',
        #         '4-f1',
        #         '4-f2'
        #     ]:
        #         if criterio in doc['form']['2017']:
        #             worksheet.write(row, col, doc['form']['2017'][criterio])
        #         col += 1
        # else:
        #     col += 7

        # 4-f3 e 4-f4
        # if 'times' in doc:
        #     # sub_aprov
        #     if 'media_meses_sub_aprov_2017' in doc['times']:
        #         times = timesfmt(doc['times']['media_meses_sub_aprov_2017'])
        #         worksheet.write(row, col, times)
        #     col += 1
        #     # aprov_pub_scielo
        #     if 'media_meses_aprov_pub_scielo_2017' in doc['times']:
        #         times = timesfmt(
        #             doc['times']['media_meses_aprov_pub_scielo_2017'])
        #         worksheet.write(row, col, times)
        #     col += 1
        # else:
        #     col += 2

        # Avança journal
        row += 1


# Ativos neste ano e inclusos antes de 2016,
def datatoform():
    # já considera:
    # title_current_status='current'
    # collection='scl'
    scielo = models.Scielofapesp.objects.filter(
        fapesp_evaluation__2018__evaluated=1)
    today = datetime.datetime.now().strftime('%Y%m%d')
    filename = 'data_to_form_' + today + '.xlsx'
    sheetname = 'toform'

    journal(query=scielo, filename=filename, sheetname=sheetname)


def main():
    datatoform()


if __name__ == "__main__":
    main()
