# coding: utf-8
'''
This script get the thematic areas(category) from a worksheet,
country and publisher from other sources and saves in the Wos collection.
'''
import models

import logging
import pyexcel


logging.basicConfig(
    filename='logs/wos_loader.info.txt',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def wos_loader():
    sheet = pyexcel.get_sheet(
        file_name='data/wos/ESIMasterJournalList-022018.xlsx',
        name_columns_by_row=0)

    wos_json = sheet.to_records()

    models.Wos.drop_collection()

    for rec in wos_json:
        print(rec['full_title'])

        rec['title'] = rec['full_title']

        rec['issn_list'] = []

        if rec['issn']:
            rec['issn_list'].append(rec['issn'])

        if rec['eissn']:
            if rec['eissn'] not in rec['issn_list']:
                rec['issn_list'].append(rec['eissn'])

        # save
        mdata = models.Wos(**rec)
        mdata.save()

    num_posts = models.Wos.objects().count()
    msg = u'Registred %d posts in Wos collection' % num_posts
    logger.info(msg)
    print(msg)


def main():
    wos_loader()

if __name__ == "__main__":
    main()
