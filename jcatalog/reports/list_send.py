# coding: utf-8
import models
import xlsxwriter

workbook = xlsxwriter.Workbook('output/lista_emails_avalia_scielo_fapesp.xlsx')
worksheet = workbook.add_worksheet('emails_editores')

# Filtras SciELO Brasil, current, entrada no scielo antes de 2016
query = models.Scielofapesp.objects.filter(fapesp_evaluation__2018__evaluated=1)

counter = 0

row = 0

for j in query:

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
