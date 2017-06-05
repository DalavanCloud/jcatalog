# coding: utf-8
'''
This script get data from DOAJ API and store in MongoDB.
'''
import os 
import sys
import models
import logging
import requests


PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename='logs/doajapi.info.txt',level=logging.INFO)
logger = logging.getLogger(__name__)


models.Doajapi.drop_collection()


for doc in models.Scielo.objects():

    flag = 0
    
    for issn in doc.issn_list:

        if flag == 0:

            r = requests.get('https://doaj.org/api/v1/search/journals/issn:%s' % issn)
            
            docdoaj = r.json()
            
            if docdoaj['total'] > 0:
                docdoaj['issn_list'] = [issn]
                mdata = models.Doajapi(**docdoaj)
                mdata.save()
                flag = 1
                msg = 'ISSN: %s found' % (issn)
                logger.info(msg)
                print(msg)
            else:
                msg = 'ISSN: %s not found' % (issn)
                logger.info(msg)
                print(msg)
