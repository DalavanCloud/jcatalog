# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import os
import pyexcel
import logging
import json

import models
from transform_date import *
from accent_remover import *

logging.basicConfig(filename='logs/aff.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


# Add manuscripts for journals
def manus(filename):
    sheet = pyexcel.get_sheet(
        file_name=filename,
        sheet_name='import',
        name_columns_by_row=0)

    sheet_json = sheet.to_records()

    for rec in sheet_json:
        print(rec['issn_scielo'])

        query = models.Scielofapesp.objects.filter(issn_scielo=rec['issn_scielo'])

        if len(query) == 1 and 'manuscritos' not in query[0]:

            doc = query[0]
            print(query[0]['issn_scielo'])
            data = {'manuscritos': {}}
            data['manuscritos'] = dict(rec)

            if data:
                doc.modify(**data)
                # doc.save()
        else:
            if len(query) == 1:
                doc = query[0]
                data = {'manuscritos': ''}
                data['manuscritos'] = json.loads(query[0].to_json())['manuscritos']
                for k, v in rec.items():
                    if k not in data['manuscritos']:
                        data['manuscritos'][k] = rec[k]
            if data:
                doc.update(**data)


def main():
    # SciELO docs counts Network xlsx
    filelist = [f for f in os.listdir('data/scielo/manuscritos/') if 'xlsx' in f]

    filelist.sort()

    for f in filelist:
        print(f)
        manus('data/scielo/manuscritos/'+f)


if __name__ == "__main__":
    main()
