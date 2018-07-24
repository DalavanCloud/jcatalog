# coding: utf-8
import os
import pyexcel

from cleaner import *
from accent_remover import *
import models


def renamer(filename):
    # sheet = pyexcel.get_sheet(
    #     file_name=filename,
    #     sheet_name='toform',
    #     name_columns_by_row=0)

    # sheet_json = sheet.to_records()

    os.chdir('output/journals/1_envio_fapesp_ped')

    for f in os.listdir('.'):
        # fn = cleaner(f.replace(".pdf", "").split("_")[1])
        # title_test = cleaner(f.replace(".pdf", "").split("_")[1])

        title = accent_remover(f.replace(".pdf", "").split("_")[1])
        # print('file: ' + title)

        query = models.Scielofapesp.objects.filter(
            title_country=title.lower() + "-brazil")

        if query:
            print(f + "|" + query[0]['title'] + "|" +
                  query[0]['issn_scielo'] + query[0]['api']['url'])
        else:
            print(f)

        # if title == fn:
            # print(f + ' --> ' + title)
            # os.rename(f, 'PDE_' + l['issn'] + '.pdf')
        # else:
        #     print(f + " ==NAO ACHOU==")


def main():
    filename = 'data/scielo/data_to_form_texto_20180720.xlsx'
    renamer(filename)

if __name__ == "__main__":
    main()

# na linha de comando lancar para output
# python manager.py > output/Lista de arquivos e periodicos do PDE.txt"
# fiz o xlsx e compartilhei com Denise no Drive para corrigir a mao
