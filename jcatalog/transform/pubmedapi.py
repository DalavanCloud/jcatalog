# coding: utf-8
'''
This script get data from Pubmed API and store in MongoDB.
https://www.ncbi.nlm.nih.gov/books/NBK25500/
'''
import logging
import requests

import models

logging.basicConfig(filename='logs/pubmedapi.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)

models.Pubmedapi.drop_collection()

url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'

for dbcol in (models.Scielo.objects, models.Noscielo.objects):

    for doc in dbcol():
        print(dbcol._collection.name)

        flag = 0

        for issn in doc['issn_list']:

            if flag == 0:

                data = {}

                # pubmed
                r = requests.get('%s?db=%s&term=%s[journal]&retmode=json' % (url, 'pubmed', issn))

                docpubmed = r.json()

                if int(docpubmed['esearchresult']['count']) > 0:
                    data['db_name'] = ['pubmed']
                    data['pubmed_count'] = int(docpubmed['esearchresult']['count'])

                # pmc
                r = requests.get('%s?db=%s&term=%s[journal]&retmode=json' % (url, 'pmc', issn))

                docpmc = r.json()

                if int(docpmc['esearchresult']['count']) > 0:
                    if 'pmc' not in data['db_name']:
                        data['db_name'].append('pmc')
                    data['pmc_count'] = int(docpmc['esearchresult']['count'])

                # scielo
                if 'db_name' in data:
                    data['issn_list'] = [issn]
                    data['scielo_id'] = str(doc.id)
                    data['db_col'] = dbcol._collection.name
                    if dbcol._collection.name == 'scielo':
                        data['title_country'] = doc.title_country

                # save data
                if 'db_name' in data:
                    mdata = models.Pubmedapi(**data)
                    mdata.save()

                    msg = 'ISSN: %s found' % (issn)
                    logger.info(msg)
                    print(msg)

                    flag = 1
                else:
                    msg = 'ISSN: %s not found' % (issn)
                    logger.info(msg)
                    print(msg)
