# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import pyexcel
import logging

import models
from transform_date import *
from accent_remover import *

logging.basicConfig(filename='logs/avalicacao.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


# Add Access count for journals
def avaliacao(filename):
    aval = pyexcel.get_sheet(
        file_name=filename,
        sheet_name='title_master_scielo',
        name_columns_by_row=0)

    aval_json = aval.to_records()

    for rec in aval_json:
        # # remove empty keys
        # rec = {k: v for k, v in rec.items() if v or v == 0}
        print(rec['issn_scielo'])
        query = models.Scielo.objects.filter(issn_scielo=rec['issn_scielo'])

        if len(query) == 1:
            doc = query[0]
            print(query[0]['issn_scielo'])
            data = {'avaliacao': {}}
            data['avaliacao'] = dict(rec)

            if data:
                doc.modify(**data)
                doc.save()


def main():
    # SciELO avaliacao xlsx
    avaliacao('data/scielo/avaliacao/20161107_SciELO_TitlesMasterList.xlsx')


if __name__ == "__main__":
    main()
