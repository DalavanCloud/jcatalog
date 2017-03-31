# coding: utf-8
'''
This script perform data matching from SciELO journals with other sources.
'''
import os
import sys
import logging
import json
import datetime

PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename='logs/cwts.info.txt',level=logging.INFO)
logger = logging.getLogger(__name__)


from proc import models


def matchscielo():
    #Match SciELO
    for doc in models.Cwts.objects():
        #etapa 1 - match com ISSN
        if doc.is_scielo == 0:
            for issn in doc.issn_list:
                try:
                    docsci = models.Scielo.objects.get(issn_list=issn, collection='scl') #apenas Brasil
                    doc.modify(
                        is_scielo = 1,
                        status_current_scielo = docsci.title_current_status,
                        collection_scielo = docsci.collection,
                        title_scielo = docsci.title_at_scielo,
                        updated_at = datetime.datetime.now)
                    doc.save()
                    print('%s : %s : %s' % (issn, doc.is_scielo, doc.source_title))
                except models.Scielo.DoesNotExist:
                    pass
        
        #etapa 2 - match com titulo
        if doc.is_scielo == 0:
            try:
                docsci = models.Scielo.objects.get(title_at_scielo_country=doc.title_and_country_scimago, collection='scl') #apenas Brasil
                doc.modify(
                    is_scielo = 1,
                    status_current_scielo = docsci.title_current_status,
                    collection_scielo = docsci.collection,
                    title_scielo = docsci.title_at_scielo,
                    updated_at = datetime.datetime.now)
                doc.save()
                print('%s : %s : %s' % (doc.is_scielo, doc.source_title, docsci.title_at_scielo))
            except models.Scielo.DoesNotExist:
                pass


def matchscimago():
    for doc in models.Cwts.objects():
        #etapa 1 - match com ISSN
        if doc.is_scimago == 0:
            for issn in doc.issn_list:
                try:
                    print(issn)
                    docsmago = models.Scimago.objects.get(issn_list=issn)
                    doc.modify(
                        is_scimago = 1,
                        title_scimago = docsmago.title,
                        updated_at = datetime.datetime.now)
                    doc.save()
                    print('%s : %s : %s' % (issn, doc.is_scimago, doc.source_title))
                except models.Scimago.DoesNotExist:
                    pass
        
        #etapa 2 - match com titulo
        if doc.is_scimago == 0:
            try:
                print(issn)
                docsmago = models.Scimago.objects.get(title=doc.title_and_country_scimago)
                doc.modify(
                    is_scimago = 1,
                    title_scimago = docsmago.title,
                    updated_at = datetime.datetime.now)
                doc.save()
                print('%s : %s : %s' % (doc.is_scimago, doc.source_title, docsmago.title_at_scielo))
            except models.Scimago.DoesNotExist:
                pass

def main():
    matchscielo()
    matchscimago()

if __name__ == "__main__":
    main()
