# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import os
import sys
import models
import pyexcel
import keycorrection
import collections_scielo
import logging
from transform import *
from accent_remover import *

PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename='logs/procstore.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


def scieloproc():
    scielo_sheet  = pyexcel.get_sheet(file_name='data/scielo/journals_scl.csv', name_columns_by_row=0)

    # Key correction
    for i, k in enumerate(keycorrection.scielo_columns_names):
        scielo_sheet.colnames[i] = k

    scielo_json = scielo_sheet.to_records()

    models.Scielo.drop_collection()

    for rec in scielo_json:

        rec['country'] = collections_scielo.country[rec['collection']]

        rec['title_country'] = '%s-%s' % (accent_remover(rec['title']).lower(), rec['country'].lower())

        # convert issn int type to str type
        if type(rec['issns']) != str:
            rec['issns'] = Issn().issn_hifen(rec['issns'])
            msg = u'issn modificado: %s - %s' % (rec['issns'], rec['title'])
            logger.info(msg)

        # convert in list
        if type(rec['issns']) == str:
            rec['issns'] = rec['issns'].split(';')
            rec['issn_list'] = []
            rec['issn_list'].append(rec['issn_scielo'])
            for i in rec['issns']:
                if i not in rec['issn_scielo']:
                    rec['issn_list'].append(i)

        # transform data in datetime type
        rec['date_of_the_first_document'] = Dates().data2datetime(rec['date_of_the_first_document'])
        rec['date_of_the_last_document'] = Dates().data2datetime(rec['date_of_the_last_document'])

        # remove empty keys
        rec = {k: v for k, v in rec.items() if v or v == 0}

        mdata = models.Scielo(**rec)
        mdata.save()

    num_posts = models.Scielo.objects().count()
    msg = u'Registred %d posts in SciELO collection' % num_posts
    logger.info(msg)
    print(msg)


def doajproc():
    doaj_sheet = pyexcel.get_sheet(file_name='data/doaj/controle_DOAJ.xlsx', name_columns_by_row=0)

    # Key correction
    for i, k in enumerate(keycorrection.doaj_columns_names):
        doaj_sheet.colnames[i] = k

    doaj_json = doaj_sheet.to_records()

    models.Doaj.drop_collection()

    for rec in doaj_json:

        rec['issn_list'] = []
        rec['issn_list'].append(rec['issn'])

        rec = { k : v for k,v in rec.items() if v} #remove empty keys

        mdata = models.Doaj(**rec)
        mdata.save()

    num_posts = models.Doaj.objects().count()
    msg = u'Registred %d posts in DOAJ collection' % num_posts
    logger.info(msg)
    print(msg)


def submissions():# Add OJS and ScholarOne
    submiss_sheet = pyexcel.get_sheet(file_name='data/submiss/sistemas_submissao_scielo_brasil.xlsx', name_columns_by_row=0)

    # Key correction
    for i, k in enumerate(keycorrection.submission_scielo_brasil_columns_names):
        submiss_sheet.colnames[i] = k

    submiss_json = submiss_sheet.to_records()

    models.Submissions.drop_collection()

    for rec in submiss_json:

        rec['issn_list'] = []
        rec['issn_list'].append(rec['issn_scielo'])

        # remove empty keys
        rec = {k: v for k, v in rec.items() if v or v == 0}

        mdata = models.Submissions(**rec)
        mdata.save()

    num_posts = models.Submissions.objects().count()
    msg = u'Registred %d posts in Submissions collection' % num_posts
    logger.info(msg)
    print(msg)


def capes():
    capes_sheet = pyexcel.get_sheet(file_name='data/capes/classificações_publicadas_todas_as_areas_avaliacao1495226039817.csv', name_columns_by_row=0, encoding='iso-8859-1', delimiter='\t')

    # Key correction
    for i, k in enumerate(keycorrection.capes_columns_names):
        capes_sheet.colnames[i] = k

    capes_json = capes_sheet.to_records()

    models.Capes.drop_collection()

    for rec in capes_json:

        rec['title_country'] = '%s-brazil' % (accent_remover(rec['title']).lower())

        rec['issn_list'] = []
        rec['issn_list'].append(rec['issn'])

        # remove empty keys
        rec = {k: v for k, v in rec.items() if v or v == 0}

        mdata = models.Capes(**rec)
        mdata.save()

    num_posts = models.Capes.objects().count()
    msg = u'Registred %d posts in Capes collection' % num_posts
    logger.info(msg)
    print(msg)


def main():
    # SciELO - csv
    scieloproc()

    # DOAJ - xlsx
    doajproc()

    # Submissions - xlsx
    submissions()

    # Capes - Qualis - xls(csv delimiter = \t)
    capes()

if __name__ == "__main__":
    main()
