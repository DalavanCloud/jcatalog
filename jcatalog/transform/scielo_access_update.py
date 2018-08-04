# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import logging
import models

import pyexcel


logging.basicConfig(filename='logs/access.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


# Add Access count for journals
def scieloaccess(filename):
    access = pyexcel.get_sheet(
        file_name=filename,
        sheet_name='import',
        name_columns_by_row=0)

    access_json = access.to_records()

    for rec in access_json:
        # # remove empty keys
        # rec = {k: v for k, v in rec.items() if v or v == 0}
        print(rec['issn'])
        query = models.Scielo.objects.filter(issn_scielo=rec['issn'])

        if len(query) == 1:
            doc = query[0]
            print(query[0]['issn_scielo'])
            data = {'access': {}}
            data['access'] = dict(rec)

            if data:
                doc.modify(**data)


def main():
    # SciELO access counts xlsx
    # scieloaccess('data/scielo/accesses_by_journals_network_180317.xlsx')
    scieloaccess(
        'data/scielo/scielo20-network/td_accesses_by_journals-network.xlsx')


if __name__ == "__main__":
    main()
