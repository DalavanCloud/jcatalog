# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import pyexcel
import logging
import json

import models
from accent_remover import *


logging.basicConfig(filename='logs/wos_indexes.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


def indexes(filename):
    sheet = pyexcel.get_sheet(
        file_name=filename,
        sheet_name='import',
        name_columns_by_row=0)

    sheet_json = sheet.to_records()

    models.Wosindexes.drop_collection()

    for rec in sheet_json:

        print(rec['issn'])

        query = models.Wosindexes.objects.filter(issn_list=rec['issn'])

        if len(query) == 0:

            rec['issn_list'] = []

            rec['issn_list'].append(rec['issn'])

            rec['indexes'] = []

            # rec['country'] = 'Brazil'
            # rec['title_country'] = '%s-%s' % (
            #     accent_remover(rec['title']).lower().replace(' & ', ' and ').replace('&', ' and '),
            #     'brazil')

            if any(rec['index'] == i for i in ['scie', 'ssci', 'ahci']):
                rec['is_wos'] = 1
            else:
                rec['is_wos'] = 0

            rec['indexes'].append(rec['index'])

            del rec['index']

            mdata = models.Wosindexes(**rec)
            mdata.save()

        else:
            if len(query) == 1:
                print('ja existe\n')

                print(rec['issn'])

                doc = query[0]

                data = {'indexes': []}

                data['indexes'] = json.loads(query[0].to_json())['indexes']
                data['indexes'].append(rec['index'])

                if data:
                    doc.update(**data)


def main():
    # SciELO
    indexes('data/incites/import_wos_indexes.xlsx')


if __name__ == "__main__":
    main()
