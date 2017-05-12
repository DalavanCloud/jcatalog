# coding: utf-8
'''
This script perform data matching from Scimago journals with other sources.
'''
import os
import sys
import logging
import datetime

PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename = 'logs/matchscimago.info.txt',level = logging.INFO)
logger = logging.getLogger(__name__)

from proc import models

# Scimago
def match_scielo(): 
    for doc in models.Scimago.objects():
        if doc.is_scielo == 0:
            for issn in doc.issn_list:
                try:
                    docsci = models.Scielo.objects.get(issn_list = issn)
                    doc.modify(
                        is_scielo = 1,
                        scielo_id = str(docsci.id),
                        updated_at = datetime.datetime.now)
                    doc.save() # save in Scimago Collection

                    msg = 'ISSN Scimago: %s is SciELO' % (issn)
                    logger.info(msg)
                    print(msg)

                except models.Scielo.DoesNotExist:
                    pass

        if doc.is_scielo == 0:
            try:
                docsci = models.Scielo.objects.get(title_at_scielo_country__iexact = doc.title_country)
                doc.modify(
                    is_scielo = 1,
                    scielo_id = str(docsci.id),
                    updated_at = datetime.datetime.now)
                doc.save() # save in Scimago Collection

                msg = 'Title-Country Scimago: %s is SciELO' % (doc.title_country)
                logger.info(msg)
                print(msg)

            except models.Scielo.DoesNotExist:
                pass


def match_wos():
    for doc in models.Scimago.objects():
        if doc.is_wos == 0:
            for issn in doc.issn_list:
                try:
                    docwos = models.Wos.objects.get(issn_list = issn)
                    doc.modify(
                        is_wos = 1,
                        wos_id = str(docwos.id),
                        updated_at = datetime.datetime.now)
                    doc.save() # save in Scimago Collection

                    msg = 'ISSN Scimago: %s is WOS' % (issn)
                    logger.info(msg)
                    print(msg)

                except models.Wos.DoesNotExist:
                    pass

        if doc.is_wos == 0:
            try:
                docwos = models.Wos.objects.get(title_country__iexact = doc.title_country)
                doc.modify(
                    is_wos = 1,
                    wos_id = str(docwos.id),
                    updated_at = datetime.datetime.now)
                doc.save() # save in Scimago Collection

                msg = 'Title-Country Scimago: %s is WOS' % (doc.title_country)
                logger.info(msg)
                print(msg)

            except models.Wos.DoesNotExist:
                pass


def match_scopus():
    for doc in models.Scimago.objects():
        if doc.is_scopus == 0:
            for issn in doc.issn_list:
                try:
                    docscopus = models.Scopus.objects.get(issn_list = issn)
                    doc.modify(
                        is_scopus = 1,
                        scopus_id = str(docscopus.id),
                        updated_at = datetime.datetime.now)
                    doc.save() # save in Scimago Collection

                    msg = 'ISSN Scimago: %s is Scopus' % (issn)
                    logger.info(msg)
                    print(msg)

                except models.Scopus.MultipleObjectsReturned:
                    docscopus = models.Scopus.objects.filter(issn_list = issn)
                    doc.modify(
                        is_scopus = 1,
                        scopus_id = str(docscopus[0].id),
                        updated_at = datetime.datetime.now)
                    doc.save() # save in Scimago Collection

                    msg = 'ISSN DUPLICADO: %s em Scopus' % (issn)
                    logger.info(msg)
                    print(msg)
                    pass

                except models.Scopus.DoesNotExist:
                    pass
        
        if doc.is_scopus == 0:
            try:
                docscopus = models.Scopus.objects.get(title_country__iexact = doc.title_country)
                doc.modify(
                    is_scopus = 1,
                    scopus_id = str(docscopus.id),
                    updated_at = datetime.datetime.now)
                doc.save() # save in Scimago Collection

                msg = 'Title-Country Scimago: %s is Scopus' % (doc.title_country)
                logger.info(msg)
                print(msg)

            except models.Scopus.MultipleObjectsReturned:
                docscopus = models.Scopus.objects.filter(title_country__iexact = doc.title_country)
                doc.modify(
                    is_scopus = 1,
                    scopus_id = str(docscopus[0].id),
                    updated_at = datetime.datetime.now)
                doc.save() # save in Scimago Collection

                msg = 'TITULO DUPLICADO: %s em Scopus' % (doc.title_country)
                logger.info(msg)
                print(msg)
                pass

            except models.Scopus.DoesNotExist:
                pass

def stats():
    print('Scimago total records: %s' % (models.Scimago.objects.count()))
    print('Scimago     is_scielo: %s' % (models.Scimago.objects.filter(is_scielo = 1).count()))
    print('Scimago     is_scopus: %s' % (models.Scimago.objects.filter(is_scopus = 1).count()))
    print('Scimago        is_wos: %s' % (models.Scimago.objects.filter(is_wos = 1).count()))


def main():
    match_scielo()
    match_wos()
    match_scopus()

    stats()

if __name__ == "__main__":
    main()
