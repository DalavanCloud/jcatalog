# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import glob

import pyexcel
import logging

import models
from accent_remover import *
from transform import collections_scielo

logging.basicConfig(filename='logs/ga_access.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)

models.Latindex.drop_collection()


def main():

    list_file = glob.glob('data/latindex/' + "*csv")

    for csvfile in list_file:
        print(csvfile)

        sheet = pyexcel.get_sheet(
            file_name=csvfile, name_columns_by_row=0, encoding='latin1')

        collection = csvfile[14:17]
        print(collection)

        # Edit labels
        labels = []
        for label in sheet.colnames:
            labels.append(accent_remover(
                label).strip().lower().replace(' ', '_'))

        for i, k in enumerate(labels):
            sheet.colnames[i] = k

        sheet_json = sheet.to_records()

        for rec in sheet_json:

            # remove empty keys
            rec = {k: v for k, v in rec.items() if v or v == 0}

            rec['issn_list'] = []

            if 'issn' in rec:
                rec['issn_list'].append(rec['issn'])

            rec['title'] = str(rec['titulo'])
            del rec['titulo']

            rec['title_lower'] = accent_remover(
                rec['title'].
                lower().
                replace(' & ', ' and ').
                replace('&', ' and '))

            # Country, Region and Titles

            rec['collection'] = collection

            rec['country'] = collections_scielo.collections[collection][1]

            rec['title_country'] = '%s-%s' % (
                rec['title_lower'],
                accent_remover(rec['country'].lower()))

            mdata = models.Latindex(**rec)
            mdata.save()


if __name__ == "__main__":
    main()
