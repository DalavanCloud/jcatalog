# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import pyexcel
import json
import models


def avaliacao_tipos(filename):
    sheet = pyexcel.get_sheet(
        file_name=filename,
        sheet_name='import',
        name_columns_by_row=0)

    sheet_json = sheet.to_records()

    for rec in sheet_json:

        query = models.Scielo.objects.filter(issn_scielo=rec['issn_scielo'])

        if len(query) == 1:

            print(rec['issn_scielo'])

            doc = query[0]

            data = {'avaliacao': ''}

            data['avaliacao'] = json.loads(query[0].to_json())['avaliacao']

            data['avaliacao']['tipo_inst'] = rec['tipo_instituicao']
            data['avaliacao']['tipo_1'] = rec['tipo_1']
            data['avaliacao']['tipo_2'] = rec['tipo_2']
            data['avaliacao']['tipo_3'] = rec['tipo_3']
            data['avaliacao']['tipo_4'] = rec['tipo_4']

            if data:
                doc.update(**data)
        else:
            print("nao encontrado")


def main():
    avaliacao_tipos('data/scielo/avaliacao/tipo_instituicao_abel.xlsx')


if __name__ == "__main__":
    main()
