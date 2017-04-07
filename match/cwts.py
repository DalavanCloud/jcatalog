# coding: utf-8
'''
This script perform data matching from SciELO journals with other sources.
'''
import os
import sys
import logging
import datetime

PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename='logs/cwts.info.txt',level=logging.INFO)
logger = logging.getLogger(__name__)

from proc import models

def matchscielo():
    for doc in models.Cwts.objects():
        print(doc.issn_list)
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

                    msg = 'ISSN:%s : is title SciELO: %s' % (issn, doc.source_title)
                    logger.info(msg)
                    print(msg)
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

                msg = 'title:%s : is title SciELO: %s' % (doc.source_title, docsci.title_at_scielo)
                logger.info(msg)
                print(msg)
            except models.Scielo.DoesNotExist:
                pass


def matchscimago():
    for doc in models.Cwts.objects():
        print(doc.issn_list)
        for issn in doc.issn_list:
            #etapa 1 - match com ISSN
            if doc.is_scimago == 0:
                try:
                    docsmago = models.Scimago.objects(issn_list=issn)
                    if docsmago.count() > 0:
                        doc.modify(
                            is_scimago = 1,
                            title_scimago = docsmago[0].title,
                            updated_at = datetime.datetime.now)
                        doc.save()
                        print('ISSN: %s : is title Scimago: %s' % (issn, doc.source_title))
                except models.Scimago.DoesNotExist:
                    pass
        
            #etapa 2 - match com titulo
            if doc.is_scimago == 0:
                try:
                    docsmago = models.Scimago.objects.get(title_country=doc.title_and_country_scimago)
                    doc.modify(
                        is_scimago = 1,
                        title_scimago = docsmago.title,
                        updated_at = datetime.datetime.now)
                    doc.save()
                    print('title-country: %s : is title Scimago-country: %s' % (doc.title_and_country_scimago, docsmago.title_country))
                except models.Scimago.DoesNotExist:
                    pass

def main():
    #matchscielo()
    matchscimago()

if __name__ == "__main__":
    main()
