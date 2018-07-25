# coding: utf-8
import os
import pyexcel
import models
from shutil import copyfile


def renamer_docx(filename):
    sheet = pyexcel.get_sheet(
        file_name=filename,
        sheet_name='toform',
        name_columns_by_row=0)

    sheet_json = sheet.to_records()

    os.chdir('output/journals/forms')

    for l in sheet_json:
        # consulta issn para obter area tematica
        query = models.Scielofapesp.objects.filter(issn_list=l['issn'])
        if query:

            at = []

            if query[0]['title_is_multidisciplinary'] == 1:
                at.append("Multidisciplinary")
            else:
                ats = query[0]['title_thematic_areas'].replace(
                    " ", "_").replace(",", "")
                at = [a for a in ats.split(';')]

            for a in at:
                # print(a)
                origem = str(l['file_name']) + '.docx'
                destino = 'Formulario-avaliacao-Fapesp-SciELO-' + \
                    a + '-' + l['issn'] + '-20180723.docx'
                print(origem + ' -->  ' + destino)
                #  copyfile(origem, 'renomeado/' + destino)


def renamer_pdf(filename):
    sheet = pyexcel.get_sheet(
        file_name=filename,
        sheet_name='toform',
        name_columns_by_row=0)

    sheet_json = sheet.to_records()

    os.chdir('output/journals/forms/pdfs')

    for l in sheet_json:
        for f in os.listdir('.'):
            if str(l['file_name']) + '.pdf' == f:
                print(str(l['file_name']) + '.pdf --> ' +
                      'Formulario-avaliacao-Fapesp-SciELO-' + l['issn'] + '-20180713.pdf')
                copyfile(f, 'renomeado/Formulario-avaliacao-Fapesp-SciELO-' +
                         l['issn'] + '-20180713.pdf')


def main():
    filename = 'data/scielo/data_to_form_texto_20180720.xlsx'

    renamer_docx(filename)

    # renamer_pdf(filename)

if __name__ == "__main__":
    main()
