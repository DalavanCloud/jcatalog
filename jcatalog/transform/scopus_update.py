# coding: utf-8
'''
This script reads data from Scopus CiteScore
to process and update Scopus collections in MongoDB.
'''
import logging
import pyexcel

import models
import keycorrection
from accent_remover import *


logging.basicConfig(filename='logs/scopus_update.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


def scopuscs(filename, year):
    scopus_sheet = pyexcel.get_sheet(
        file_name=filename,
        sheet_name=year + ' All',
        name_columns_by_row=0)

    print(year)

    # Key correction
    for i, k in enumerate(keycorrection.scopuscitscore_columns_names):
        scopus_sheet.colnames[i] = k

    scopus_sheet.column.format('print_issn', str)
    scopus_sheet.column.format('eissn', str)
    scopus_json = scopus_sheet.to_records()

    for rec in scopus_json:

        # remove empty keys
        rec = {k: v for k, v in rec.items() if v or v == 0}

        query = models.Scopus.objects.filter(
            sourcerecord_id=rec['scopus_sourceid'])

        if len(query) == 1:

            data = {}

            for k in ['citescore', 'sjr', 'snip']:

                if year not in data and k in rec:
                    data = {year: {}}

                if k in rec and rec[k] != '':
                    data[year].update({k: float(rec[k])})

            if len(data) > 0:
                query[0].modify(**data)
                query[0].save()


def main():

    filename = 'data/scopus/CiteScore_Metrics_2011-2016_Download_06Feb2018.xlsx'

    # Updates from year 2011 to 2013
    for year in range(2011, 2014):
        scopuscs(filename, str(year))

if __name__ == "__main__":
    main()
