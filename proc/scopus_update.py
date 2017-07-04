# coding: utf-8
'''
This script add citescore, sjr and snip 2016 indicators in Scopus collection at MongoDB
'''
import os
import sys
import logging

from mongoengine import *

PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename='logs/matches.scopuscitescore.txt', level=logging.INFO)
logger = logging.getLogger(__name__)

from proc import models

for doc in models.Scopuscitescore.objects().batch_size(5):

    query = models.Scopus.objects.filter(sourcerecord_id = doc.scopus_sourceid)

    if len(query) == 1:
        
        for k in ['sjr', 'citescore', 'snip']:
            if k in doc:    
                data = {'i2016_' +  k : doc[k]}
                
                query[0].modify(**data)
                query[0].save()  # save in Scopuscitescore

        msg = str(len(query)) + ' = ' + doc.title
        logger.info(msg)
        print(msg)
