# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import pyexcel
import logging

import models

logging.basicConfig(filename='logs/docs.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


# Add documents count for journals
def docs(filename):
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
            data = {'docs': {}}
            data['docs'] = dict(rec)

            if data:
                doc.modify(**data)


def main():
    # SciELO docs counts Network xlsx
    # docs('data/scielo/documents_languages_network_180317.xlsx')
    # docs('data/scielo/scielo20-network/td_documents_languages_network.xlsx')
    docs('extractors/scielo/output/td_documents_languages_bra_190123.xlsx')


if __name__ == "__main__":
    main()
