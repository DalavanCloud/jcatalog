# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import pyexcel
import logging
import json

import models

logging.basicConfig(filename='logs/altmetrics.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


# Add Access count for journals
def scielogaaccess(filename, sheetname, year):
    altmetrics = pyexcel.get_sheet(
        file_name=filename,
        sheet_name=sheetname,
        name_columns_by_row=0)

    # Edit labels
    labels = []
    for t in altmetrics.colnames:
        labels.append(
            t.strip().lower().
            replace(", ", "_").
            replace(' ', '_').
            replace("'", "").
            replace("(", "").
            replace(")", "")
        )

    for i, k in enumerate(labels):
        altmetrics.colnames[i] = k

    altmetrics_json = altmetrics.to_records()

    for rec in altmetrics_json:
        # remove empty keys
        rec = {k: v for k, v in rec.items() if v or v == 0}

        # rec['issns'] = rec['issns'].split(';')
        rec['issn_list'] = []
        if 'issn1' in rec:
            rec['issn_list'].append(rec['issn1'].strip())
        if 'issn2' in rec:
            rec['issn_list'].append(rec['issn2'].strip())

        print(rec['issn_list'])

        for issn in rec['issn_list']:

            flag = 0

            query = models.Scielo.objects.filter(issn_scielo=issn)

            if len(query) == 1 and flag == 0:
                doc = query[0]
                print(query[0]['issn_scielo'])

                data = {}
                if 'altmetrics' in doc:
                    data['altmetrics'] = json.loads(
                        query[0].to_json())['altmetrics']
                    data['altmetrics'][year] = dict(rec)
                else:
                    data['altmetrics'] = {}
                    data['altmetrics'][year] = dict(rec)
                if data:
                    doc.modify(**data)
                    flag = 1


def main():
    # Altmetrics
    scielogaaccess(
        'data/scielo/altmetrics/Altmetric-SciELO journals - 20170601-20183005.xlsx',
        'import', '2018')


if __name__ == "__main__":
    main()
