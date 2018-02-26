# coding: utf-8
'''
This script reads data from Scopus xlsx files to process and laod in MongoDB.
'''
import logging
import pyexcel

import models
import keycorrection
from accent_remover import *

logging.basicConfig(filename='logs/scopus_loader.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


def scopus_loader(file_name, keycorrection):

    models.Scopus.drop_collection()

    sheet = pyexcel.get_sheet(file_name=file_name, name_columns_by_row=0)

    # Key correction
    for i, k in enumerate(keycorrection):
        sheet.colnames[i] = k

    sheet.column.format('print_issn', str)
    sheet.column.format('e_issn', str)
    sheet_json = sheet.to_records()

    for rec in sheet_json:

        if type(rec['sourcerecord_id']) == str:
            rec['sourcerecord_id'] = int(rec['sourcerecord_id'])

        rec['country'] = rec['publishers_country']

        rec['title_country'] = '%s-%s' % (
            accent_remover(rec['title']).lower().replace(' & ', ' and ').replace('&', ' and '),
            rec['publishers_country'].lower())

        rec['issn_list'] = []

        if rec['print_issn']:
            rec['issn_list'].append(rec['print_issn'][0:4] + '-' + rec['print_issn'][4:8])

        if rec['e_issn']:
            rec['issn_list'].append(rec['e_issn'][0:4] + '-' + rec['e_issn'][4:8])

        # remove empty keys
        rec = {k: v for k, v in rec.items() if v or v == 0}

        for year in ['2014', '2015', '2016']:

            for k in ['citescore', 'sjr', 'snip']:

                if k+'_'+year in rec:

                    if year not in rec:

                        rec[year] = {}

                    rec[year].update({k: float(rec[k+'_'+year])})

                    del rec[k+'_'+year]

        # Codes ASJC
        codes = []
        codes = rec['all_science_classification_codes_asjc'].replace(' ', '').split(';')
        for c in codes:
            if c == '':
                codes.pop()
        rec['asjc_code_list'] = codes

        # Save data
        mdata = models.Scopus(**rec)
        mdata.save()

    num_posts = models.Scopus.objects().count()
    msg = u'Registred %d posts in Scopus collection' % num_posts
    logger.info(msg)
    print(msg)


def main():
    '''
    scopus_loader(file_name, keycorrection)
        file_name = xlsx path and file name
    keycorrection = dict name of keycorrection module
    '''
    scopus_loader(
        'data/scopus/ext_list_October_2017.xlsx',
        keycorrection.scopus_columns_names)


if __name__ == "__main__":
    main()
