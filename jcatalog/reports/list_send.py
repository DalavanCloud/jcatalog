# coding: utf-8
import models
import xlsxwriter

workbook = xlsxwriter.Workbook('output/lista_emails_avalia_scielo_fapesp.xlsx')
worksheet = workbook.add_worksheet('lista_emails_editores')

query = models.Scielo.objects.filter(
    title_current_status='current',
    collection='scl')
counter = 0

row = 0

# Filtras SciELO Brasil, current, entrada no scielo antes de 2016
for j in query:
    docs16 = 0
    entrada = 0
    ativo_y = 0

    if 'docs' in j:
        if j['docs']['docs_2016'] == '':
            pass
        elif j['docs']['docs_2016'] > 0:
            docs16 = 1

        for year in range(2007, 2019):
            y = str(year)
            if 'docs_'+y in j['docs']:
                if j['docs']['docs_'+y] == '':
                    pass
                elif int(j['docs']['docs_'+y]) > 0:
                    ativo_y = 1
                    break

    if j['inclusion_year_at_scielo'] < 2016:
        entrada = 1

    if docs16 == 1 and entrada == 1 and ativo_y == 1:

        worksheet.write(row, 0, j['issn_scielo'])
        worksheet.write(row, 1, j['title'])

        if 'avaliacao' in j:
            if 'contatos' in j['avaliacao']:
                worksheet.write(row, 2, ','.join([e['email_address'] for e in j['avaliacao']['contatos']]))
        else:
            print(j['issn_scielo'] + "sem email")

        worksheet.write(row, 3, 'http://static.scielo.org/fapesp_evaluation/avaliacao_scielo_'+j['issn_scielo']+'.xlsx')

        row += 1

workbook.close()
