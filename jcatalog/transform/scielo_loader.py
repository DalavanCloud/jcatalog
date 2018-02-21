# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import pyexcel
import logging

import keycorrection
from transform import collections_scielo
import models
from transform_date import *
from accent_remover import *
from articlemeta.client import ThriftClient

logging.basicConfig(filename='logs/procstore.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


def scieloproc():
    scielo_sheet = pyexcel.get_sheet(
        file_name='data/scielo/journals.csv',
        name_columns_by_row=0)

    # Key correction
    for i, k in enumerate(keycorrection.scielo_columns_names):
        scielo_sheet.colnames[i] = k

    scielo_json = scielo_sheet.to_records()

    models.Scielo.drop_collection()

    for rec in scielo_json:

        rec['country'] = collections_scielo.collection[rec['collection']]

        rec['title_country'] = '%s-%s' % (
            accent_remover(rec['title']).lower().replace(' & ', ' and ').replace('&', ' and '),
            rec['country'].lower())

        # convert issn int type to str type
        if type(rec['issns']) != str:
            rec['issns'] = Issn().issn_hifen(rec['issns'])
            msg = u'issn converted: %s - %s' % (rec['issns'], rec['title'])
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

        rec['collections'] = []
        rec['collections'].append(rec['collection'])

        # remove empty keys
        rec = {k: v for k, v in rec.items() if v or v == 0}

        if rec['collection'] not in ['sss', 'rve', 'psi']:
            mdata = models.Scielo(**rec)
            mdata.save()

    num_posts = models.Scielo.objects().count()
    msg = u'Registred %d posts in SciELO collection' % num_posts
    logger.info(msg)
    print(msg)


def scieloapi():

    client = ThriftClient()

    for journal in client.journals():

        query = models.Scielo.objects.filter(issn_scielo=journal.scielo_issn)

        if query:

            for doc in query:
                print('api: ' + journal.scielo_issn)
                data = {'api': {}}

                for label in keycorrection.scielo_api:

                    try:
                        if label == 'url':
                            jdata = getattr(journal, label)()
                        else:
                            jdata = getattr(journal, label)
                        if jdata and jdata is not None:
                            data['api'][label] = jdata
                    except ValueError:
                        continue

                if data:
                    doc.modify(**data)
                    doc.save()


def doajproc():
    doaj_sheet = pyexcel.get_sheet(
        file_name='data/doaj/controle_DOAJ.xlsx',
        name_columns_by_row=0)

    # Key correction
    for i, k in enumerate(keycorrection.doaj_columns_names):
        doaj_sheet.colnames[i] = k

    doaj_json = doaj_sheet.to_records()

    models.Doaj.drop_collection()

    for rec in doaj_json:

        rec['issn_list'] = []
        rec['issn_list'].append(rec['issn'])

        # remove empty keys
        rec = {k: v for k, v in rec.items() if v or v == 0}

        mdata = models.Doaj(**rec)
        mdata.save()

    num_posts = models.Doaj.objects().count()
    msg = u'Registred %d posts in DOAJ collection' % num_posts
    logger.info(msg)
    print(msg)


# Add OJS and ScholarOne
def submissions():
    submiss_sheet = pyexcel.get_sheet(
        file_name='data/submiss/sistemas_submissao_scielo_brasil.xlsx',
        name_columns_by_row=0)

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


def main():
    # SciELO Network csv
    scieloproc()

    # SciELO Articlemeta API
    scieloapi()

    # DOAJ - xlsx
    doajproc()

    # Submissions - xlsx
    submissions()


if __name__ == "__main__":
    main()
