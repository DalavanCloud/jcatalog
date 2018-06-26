# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import pyexcel
import logging

import models
from accent_remover import *

logging.basicConfig(filename='logs/orcid.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


def orcid(filename):
    sheet = pyexcel.get_sheet(
        file_name=filename,
        sheet_name='import',
        name_columns_by_row=0)

    sheet_json = sheet.to_records()

    for rec in sheet_json:
        query = models.Scielo.objects.filter(collection='scl', title=rec['title'])

        if len(query) == 1:
            doc = query[0]
            data = {}
            data['orcid'] = 1
            if data:
                doc.update(**data)
        else:
            print('---Nao encontrado: ' + rec['title'])


def main():
    orcid('data/scielo/SciELO-ScholarOne-ORCID.xlsx')


if __name__ == "__main__":
    main()
