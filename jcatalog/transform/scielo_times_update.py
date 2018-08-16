# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import pyexcel
import logging

import models
from transform_date import *
from accent_remover import *

logging.basicConfig(filename='logs/times.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


def times(filename):
    sheet = pyexcel.get_sheet(
        file_name=filename,
        sheet_name='import',
        name_columns_by_row=0)

    sheet_json = sheet.to_records()

    for rec in sheet_json:
        # # remove empty keys
        # rec = {k: v for k, v in rec.items() if v or v == 0}
        print(rec['issn_scielo'])
        query = models.Scielo.objects.filter(issn_scielo=rec['issn_scielo'])

        if len(query) == 1:
            doc = query[0]
            print(query[0]['issn_scielo'])
            data = {'times': {}}
            data['times'] = dict(rec)

            if data:
                doc.modify(**data)


def main():
    # times('data/scielo/td_documents_dates_abel_entrada_scielo_mi.xlsx')
    times('data/scielo/td_dates.xlsx')


if __name__ == "__main__":
    main()
