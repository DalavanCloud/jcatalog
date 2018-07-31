# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import datetime
import pyexcel
import logging
import json
import requests

import re
import keycorrection
from transform import collections_scielo
import models
from transform_date import *
from accent_remover import *
from cleaner import *
from articlemeta.client import ThriftClient

logging.basicConfig(filename='logs/scielo_update.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)

client = ThriftClient()


def scieloupdate():
    scielo_sheet = pyexcel.get_sheet(
        file_name='data/scielo/journals_net.csv',
        name_columns_by_row=0)

    # Edit labels
    labels = []
    for t in scielo_sheet.colnames:
        labels.append(
            t.strip().lower().
            replace(" + ", "_").
            replace(", ", "_").
            replace(' ', '_').
            replace("'", "").
            replace("(", "").
            replace(")", "")
        )

    for i, k in enumerate(labels):
        scielo_sheet.colnames[i] = k

    scielo_json = scielo_sheet.to_records()

    for rec in scielo_json:
        # remove empty keys
        rec = {k: v for k, v in rec.items() if v or v == 0}
        print(rec['issn_scielo'])

        # Title
        rec['title'] = rec['title_at_scielo']

        rec['title_lower'] = accent_remover(
            rec['title_at_scielo'].lower().replace(
                ' & ', ' and ').replace('&', ' and '))

        rec['title_clean'] = cleaner(rec['title_at_scielo'])

        # Sem dados entre Parenteses - title
        # dp = data in parentheses
        dp = None
        dp = re.search(r"\(.+?\)", rec['title'])
        if dp:
            rec['title_clean_ndp'] = cleaner(rec['title'].replace(dp[0], ""))

        # ISSNs
        if 'issns' in rec:
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
        if 'date_of_the_first_document' in rec:
            rec['date_of_the_first_document'] = Dates().data2datetime(
                rec['date_of_the_first_document'])
        if 'date_of_the_last_document' in rec:
            rec['date_of_the_last_document'] = Dates().data2datetime(
                rec['date_of_the_last_document'])

        rec['api'] = scieloapi(rec['collection'], rec['issn_scielo'])

        rec['updated_at'] = datetime.datetime.now()

        # UPDATE or SAVE
        # SPA will be loaded
        if rec['collection'] not in [
                'sss',
                'rve',
                'psi',
                'rvt']:

            query = models.Scielo.objects.filter(issn_list=rec['issn_scielo'])

            if query:
                # Collection Type
                col_type = collections_scielo.collections[
                    rec['collection']][2]
                if col_type not in query[0]['collection_type']:
                    col_types = list(query[0]['collection_type'])
                    col_types.append(col_type)
                    rec['collection_type'] = list(set(col_types))

                del rec['collection']

                doc = query[0]

                doc.modify(**rec)
            else:
                # SPA will not load
                if rec['collection'] not in [
                        'spa',
                        'sss',
                        'rve',
                        'psi',
                        'rvt']:

                    # Collection Type
                    rec['collection_type'] = []
                    rec['collection_type'].append(collections_scielo.collections[
                        rec['collection']][2])

                    # Country, Region and Titles
                    rec['country'] = collections_scielo.collection[
                        rec['collection']]

                    if 'region' not in rec and 'country' in rec:
                        rec['region'] = collections_scielo.region[
                            rec['country']]

                    rec['title_country'] = '%s-%s' % (
                        rec['title_lower'],
                        accent_remover(rec['country'].lower()))

                    rec['title_clean_country'] = '%s-%s' % (
                        rec['title_clean'],
                        accent_remover(rec['country'].lower()))

                    rec['title_clean_ndp_country'] = '%s-%s' % (
                        rec['title_clean_ndp'],
                        accent_remover(rec['country'].lower()))

                    rec['collections'] = []
                    rec['collections'].append(rec['collection'])

                    models.Scielo(**rec).save()

    num_posts = models.Scielo.objects().count()
    msg = u'Registred %d posts in SciELO collection' % num_posts
    logger.info(msg)
    print(msg)


def scieloapi(col, issn):

    journal = client.journal(collection=col, code=issn)

    if journal:
        print('api: ' + journal.scielo_issn)
        data = {}

        for label in keycorrection.scielo_api:

            try:
                if label == 'url':
                    jdata = getattr(journal, label)()
                else:
                    jdata = getattr(journal, label)
                if jdata and jdata is not None:
                    data[label] = jdata
            except ValueError:
                continue

        if data:
            return data


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


# Crossref
def crossref():

    query = models.Scielo.objects.filter()
    if query:
        for journal in query:
            doc = journal
            print(journal['issn_scielo'])
            issn = journal['issn_scielo']
            url = 'https://api.crossref.org/works?filter=issn:%s' % issn
            r = requests.get(url)
            doi = json.loads(r.text)

            # Other ISSNs
            other_issns = []

            if len(doi['message']['items']) > 1:
                print('doi')
                if 'ISSN' in doi['message']['items'][0]:
                    if issn in doi['message']['items'][0]['ISSN']:
                        jdata = {'crossref': {}}
                        jdata['crossref']['doi_provider'] = {}
                        prefix = doi['message']['items'][0]['prefix']
                        publisher = doi['message']['items'][0]['publisher']
                        jdata['crossref']['doi_provider']['prefix'] = prefix
                        jdata['crossref']['doi_provider'][
                            'publisher'] = publisher

                        for i in doi['message']['items'][0]['ISSN']:

                            if i not in journal['issn_list']:
                                other_issns.append(i)
                                print('add issn')

            if other_issns:
                jdata['crossref']['other_issns'] = other_issns

            # Save data in Mongo DB
            if jdata:
                doc.modify(**jdata)
                doc.save()
                print(jdata)


def main():
    # SciELO Network csv
    scieloupdate()

    # # SciELO Articlemeta API
    # scieloapi()

    # # DOAJ - xlsx
    # doajproc()

    # # Submissions - xlsx
    # submissions()

    # Crossref
    # crossref()


if __name__ == "__main__":
    main()
