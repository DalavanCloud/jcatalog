# coding: utf-8
import os
import pyexcel

from accent_remover import *


def renamer(filename):
    sheet = pyexcel.get_sheet(
        file_name=filename,
        sheet_name='toform',
        name_columns_by_row=0)

    sheet_json = sheet.to_records()

    os.chdir('output/journals/1_envio_fapesp_ped')

    for l in sheet_json:
        for f in os.listdir('.'):
            fn = accent_remover(
                f.replace('PDE_', '').
                replace('.pdf', '').
                replace('.', '').
                replace(' ', '').
                replace('(', '').
                replace(')', '').
                replace(',', '').
                replace('+', '').
                replace('-', '').
                replace('&', '').lower().strip())

            title = accent_remover(
                l['nome_periodico'].replace('.', '').
                replace('.', '').
                replace(' ', '').
                replace('(', '').
                replace(')', '').
                replace(',', '').
                replace('+', '').
                replace('-', '').
                replace('&', '').lower().strip())
            # print(fn)
            if title == fn:
                print(fn + ' --> ' + title)
                # os.rename(f, 'PDE_' + l['issn'] + '.pdf')

            # else:
            #     print(f + " ==NAO ACHOU====")


def main():
    filename = 'data/scielo/data_to_form_texto_20180712.xlsx'
    renamer(filename)

if __name__ == "__main__":
    main()
