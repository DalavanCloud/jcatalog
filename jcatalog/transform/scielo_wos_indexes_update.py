# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import pyexcel
import logging
import json

import models
from accent_remover import *


logging.basicConfig(filename='logs/scielo_wos_indexes.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


def indexes(filename):
    sheet = pyexcel.get_sheet(
        file_name=filename,
        sheet_name='import',
        name_columns_by_row=0)

    sheet_json = sheet.to_records()

    for rec in sheet_json:

        print(rec['issn'])

        query = models.Scielo.objects.filter(issn_list=rec['issn'])

        if len(query) == 1:

            print(query[0]['issn_scielo'])
            data = {'wos_indexes': []}
            if 'wos_indexes' in query[0]:
                data['wos_indexes'] = json.loads(query[0].to_json())['wos_indexes']

            # rec['country'] = 'Brazil'
            # rec['title_country'] = '%s-%s' % (
            #     accent_remover(rec['title']).lower().replace(' & ', ' and ').replace('&', ' and '),
            #     'brazil')

            data['wos_indexes'].append(dict(rec))

            if any(rec['index'] == i for i in ['scie', 'ssci', 'ahci']):
                data['is_wos'] = 1
            else:
                data['is_wos'] = 0

            if data:
                query[0].modify(**data)


def main():
    # SciELO
    indexes('data/incites/import_wos_indexes.xlsx')


if __name__ == "__main__":
    main()
