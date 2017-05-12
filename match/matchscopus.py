# coding: utf-8
'''
This script perform data matching from Scopus journals with other sources.
'''
import os
import sys
import logging
import datetime

PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename = 'logs/matchscopus.info.txt',level = logging.INFO)
logger = logging.getLogger(__name__)

from proc import models

# Scopus
def match_scielo(): 
    for doc in models.Scopus.objects():
        if doc.is_scielo == 0:
            for issn in doc.issn_list:
                try:
                    docsci = models.Scielo.objects.get(issn_list = issn)
                    doc.modify(
                        is_scielo = 1,
                        scielo_id = str(docsci.id),
                        updated_at = datetime.datetime.now)
                    doc.save() # save in Scopus Collection

                    msg = 'ISSN Scopus: %s is SciELO' % (issn)
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
                doc.save() # save in Scopus Collection

                msg = 'Title-Country Scopus: %s is SciELO' % (doc.title_country)
                logger.info(msg)
                print(msg)

            except models.Scielo.DoesNotExist:
                pass


def match_wos():
    for doc in models.Scopus.objects():
        if doc.is_wos == 0:
            for issn in doc.issn_list:
                try:
                    docwos = models.Wos.objects.get(issn_list = issn)
                    doc.modify(
                        is_wos = 1,
                        wos_id = str(docwos.id),
                        updated_at = datetime.datetime.now)
                    doc.save() # save in Scopus Collection

                    msg = 'ISSN Scopus: %s is WOS' % (issn)
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
                doc.save() # save in Scopus Collection

                msg = 'Title-Country Scopus: %s is WOS' % (doc.title_country)
                logger.info(msg)
                print(msg)

            except models.Wos.DoesNotExist:
                pass


def match_scimago():

    docscopus = models.Scopus.objects()

    for doc in docscopus:
        if doc.is_scimago == 0:
            for issn in doc.issn_list:
                try:
                    print(issn)
                    docsmago = models.Scimago.objects.get(issn_list = issn, no_cursor_timeout=True).batch_size(5)
                    doc.modify(
                        is_scimago = 1,
                        scimago_id = str(docsmago.id),
                        updated_at = datetime.datetime.now)
                    doc.save() # save in Scopus Collection

                    msg = 'ISSN Scopus: %s is Scimago' % (issn)
                    logger.info(msg)
                    print(msg)

                except models.Scimago.MultipleObjectsReturned:
                    docsmago = models.Scimago.objects.filter(issn_list = issn)
                    doc.modify(
                        is_scimago = 1,
                        scimago_id = str(docsmago[0].id),
                        updated_at = datetime.datetime.now)
                    doc.save() # save in Scopus Collection

                    msg = 'ISSN DUPLICADO: %s em Scimago' % (issn)
                    logger.info(msg)
                    print(msg)
                    pass

                except models.Scimago.DoesNotExist:
                    pass
        
        if doc.is_scimago == 0:
            try:
                docsmago = models.Scimago.objects.get(title_country__iexact = doc.title_country, no_cursor_timeout=True).batch_size(5)
                doc.modify(
                    is_scimago = 1,
                    scimago_id = str(docsmago.id),
                    updated_at = datetime.datetime.now)
                doc.save() # save in Scopus Collection

                msg = 'Title-Country Scopus: %s is Scimago' % (doc.title_country)
                logger.info(msg)
                print(msg)

            except models.Scimago.MultipleObjectsReturned:
                docsmago = models.Scimago.objects.filter(title_country__iexact = doc.title_country)
                doc.modify(
                    is_scimago = 1,
                    scimago_id = str(docsmago[0].id),
                    updated_at = datetime.datetime.now)
                doc.save() # save in Scopus Collection

                msg = 'TITULO DUPLICADO: %s em Scimago' % (issn)
                logger.info(msg)
                print(msg)
                pass

            except models.Scimago.DoesNotExist:
                pass

    #docscopus.close()

def stats():

    print('Scopus total records: %s' % (models.Scopus.objects.count()))
    print('Scopus     is_scielo: %s' % (models.Scopus.objects.filter(is_scielo = 1).count()))
    print('Scopus     is_scopus: %s' % (models.Scopus.objects.filter(is_scimago = 1).count()))
    print('Scopus        is_wos: %s' % (models.Scopus.objects.filter(is_wos = 1).count()))


def main():
    #match_scielo()
    #match_wos()
    match_scimago()

    stats()

if __name__ == "__main__":
    main()
