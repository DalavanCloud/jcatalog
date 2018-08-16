# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import pyexcel
import logging
import json

import models

logging.basicConfig(filename='logs/ga_access.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


# Add Access count for journals
def scielogaaccess(filename, sheetname, year):
    ga_access = pyexcel.get_sheet(
        file_name=filename,
        sheet_name=sheetname,
        name_columns_by_row=0)

    ga_access_json = ga_access.to_records()

    for rec in ga_access_json:
        # # remove empty keys
        # rec = {k: v for k, v in rec.items() if v or v == 0}
        print(rec['issn'])
        query = models.Scielo.objects.filter(issn_scielo=rec['issn'])

        if len(query) == 1:
            doc = query[0]
            print(query[0]['issn_scielo'])

            data = {}
            if 'ga_access' in doc:
                data['ga_access'] = json.loads(query[0].to_json())['ga_access']
                data['ga_access'][year] = dict(rec)
            else:
                data['ga_access'] = {}
                data['ga_access'][year] = dict(rec)
            if data:
                doc.modify(**data)


def main():
    # Google Analytics access counts
    # scielogaaccess('data/scielo/ga_scielo_year2017_20180627.xlsx')
    scielogaaccess('data/scielo/ga_scielo_year2015-2017.xlsx',
                   'import_15', '2015')


if __name__ == "__main__":
    main()
