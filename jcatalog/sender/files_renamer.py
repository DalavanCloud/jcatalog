# coding: utf-8
import os
import pyexcel


def renamer(filename):
    sheet = pyexcel.get_sheet(
        file_name=filename,
        sheet_name='toform',
        name_columns_by_row=0)

    sheet_json = sheet.to_records()

    os.chdir('output/journals/forms')

    for l in sheet_json:
        for f in os.listdir('.'):
            if str(l['pdf']) + '.pdf' == f:
                print(str(l['pdf']) + '.pdf --> ' +
                      'Formulario-avaliacao-Fapesp-SciELO-' + l['issn'] + '-20180713.pdf')
                os.rename(f, 'Formulario-avaliacao-Fapesp-SciELO-' +
                          l['issn'] + '-20180713.pdf')


def main():
    filename = 'data/scielo/data_to_form_texto_20180712.xlsx'
    renamer(filename)

if __name__ == "__main__":
    main()
