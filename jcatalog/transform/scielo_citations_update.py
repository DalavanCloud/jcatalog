# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import pyexcel
import logging
import json
import models

logging.basicConfig(filename='logs/citations.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


def citations(filename):
    sheet = pyexcel.get_sheet(
        file_name=filename,
        sheet_name='import',
        name_columns_by_row=0)

    sheet_json = sheet.to_records()

    for rec in sheet_json:
        query = models.Scielo.objects.filter(issn_list=rec['issn_scielo'])

        if len(query) == 1:
            doc = query[0]
            # print(rec['issn_scielo'])
            if 'citations' not in doc:
                data = {}
                data['citations'] = []
                data['citations'].append({str(rec['pub_year']): rec})
                if data:
                    doc.update(**data)
            else:
                data = {}
                # data['citations'] = []
                data['citations'] = json.loads(query[0].to_json())['citations']
                data['citations'].append({str(rec['pub_year']): rec})
                if data:
                    doc.update(**data)
        else:
            print('--------: ' + rec['issn_scielo'] + rec['scielo_country'])


def main():
    citations('data/scielo/B01c_en_NOVA_corrigida.xlsx')


if __name__ == "__main__":
    main()
