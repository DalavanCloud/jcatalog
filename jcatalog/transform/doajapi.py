# coding: utf-8
'''
This script get data from DOAJ API and store in MongoDB.
'''
import logging
import requests

import models

logging.basicConfig(filename='logs/doajapi.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


models.Doajapi.drop_collection()

url = 'https://doaj.org/api/v1/search/journals/issn:'

for dbcol in (
    models.Scielo.objects,
    models.Noscielo.objects
        ):

    for doc in dbcol:
        print(dbcol._collection.name)

        flag = 0
        for issn in doc['issn_list']:

            if flag == 0:

                r = requests.get(url + '%s' % issn)

                docdoaj = r.json()

                if docdoaj['total'] > 0:
                    docdoaj['issn_list'] = [issn]
                    docdoaj['scielo_id'] = str(doc.id)
                    docdoaj['title'] = docdoaj['results'][0]['bibjson']['title']
                    mdata = models.Doajapi(**docdoaj)
                    mdata.save()

                    msg = 'ISSN: %s found' % (issn)
                    logger.info(msg)
                    print(msg)

                    flag = 1
                    break

                else:
                    msg = 'ISSN: %s not found' % (issn)
                    logger.info(msg)
                    print(msg)
