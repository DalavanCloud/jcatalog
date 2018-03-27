# coding: utf-8
'''
This script reads data from xlsx file and store in MongoDB.
'''
import pyexcel
import logging

import models
from transform_date import *
from accent_remover import *

logging.basicConfig(filename='logs/apc.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


# Add Access count for journals
def apc(filename):
    apc = pyexcel.get_sheet(
        file_name=filename,
        sheet_name='import',
        name_columns_by_row=0)

    apc_json = apc.to_records()

    for rec in apc_json:
        # remove empty keys
        # rec = {k: v for k, v in rec.items() if v or v == 0}
        print(rec['issn'])
        query = models.Scielo.objects.filter(issn_scielo=rec['issn'])

        if len(query) == 1:
            doc = query[0]
            print(query[0]['issn_scielo'])
            data = {'apc': {}}
            data['apc'] = dict(rec)

            if data:
                doc.modify(**data)
                doc.save()


def main():
    # SciELO APC xlsx
    apc('data/scielo/APC-SciELO-Brasil.xlsx')


if __name__ == "__main__":
    main()
