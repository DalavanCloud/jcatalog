# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import logging

import models

import pyexcel

logging.basicConfig(
    filename='logs/dates_chl_update.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


# Add metrics of Google Scholar for journals
def creationdate(filename):

    print(filename)

    sheet = pyexcel.get_sheet(file_name=filename, sheet_name='import',
                              name_columns_by_row=0)

    sheet_json = sheet.to_records()

    for rec in sheet_json:
        # # remove empty keys
        # rec = {k: v for k, v in rec.items() if v or v == 0}
        query = models.Scielo.objects.filter(issn_list=rec['issn_scielo'])
        if query:

            doc = query[0]

            data = {}
            data['journal_creation_year'] = rec['data_criacao']
            data['journal_creation_year_verified'] = 1

            if data:
                doc.modify(**data)
        else:
            print(rec['issn_scielo'])


def main():

    creationdate('data/scielo/scielo_20_anos_data_mais_antiga-Chile-Abel.xlsx')

if __name__ == "__main__":
    main()
