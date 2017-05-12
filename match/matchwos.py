# coding: utf-8
'''
This script perform data matching from WOS journals with other sources.
'''
import os
import sys
import logging
import datetime

PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename = 'logs/matchwos.info.txt',level = logging.INFO)
logger = logging.getLogger(__name__)

from proc import models

# WOS
def match_scielo(): 
    for doc in models.Wos.objects():
        if doc.is_scielo == 0:
            for issn in doc.issn_list:
                try:
                    docsci = models.Scielo.objects.get(issn_list = issn)
                    doc.modify(
                        is_scielo = 1,
                        scielo_id = str(docsci.id),
                        updated_at = datetime.datetime.now)
                    doc.save() # save in WOS Collection

                    msg = 'ISSN WOS: %s is SciELO' % (issn)
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
                doc.save() # save in WOS Collection

                msg = 'Title-Country WOS: %s is SciELO' % (doc.title_country)
                logger.info(msg)
                print(msg)

            except models.Scielo.DoesNotExist:
                pass


def match_scimago():
    for doc in models.Wos.objects():
        if doc.is_scimago == 0:
            for issn in doc.issn_list:
                try:
                    docmago = models.Scimago.objects.get(issn_list = issn)
                    doc.modify(
                        is_scimago = 1,
                        scimago_id = str(docmago.id),
                        updated_at = datetime.datetime.now)
                    doc.save() # save in WOS Collection

                    msg = 'ISSN WOS: %s is Scimago' % (issn)
                    logger.info(msg)
                    print(msg)

                except models.Scimago.DoesNotExist:
                    pass

        if doc.is_scimago == 0:
            try:
                docmago = models.Scimago.objects.get(title_country__iexact = doc.title_country)
                doc.modify(
                    is_scimago = 1,
                    scimago_id = str(docmago.id),
                    updated_at = datetime.datetime.now)
                doc.save() # save in WOS Collection

                msg = 'Title-Country WOS: %s is Scimago' % (doc.title_country)
                logger.info(msg)
                print(msg)

            except models.Scimago.DoesNotExist:
                pass


def match_scopus():
    for doc in models.Wos.objects():
        if doc.is_scopus == 0:
            for issn in doc.issn_list:
                try:
                    docscopus = models.Scopus.objects.get(issn_list = issn)
                    doc.modify(
                        is_scopus = 1,
                        scopus_id = str(docscopus.id),
                        updated_at = datetime.datetime.now)
                    doc.save() # save in WOS Collection

                    msg = 'ISSN WOS: %s is Scopus' % (issn)
                    logger.info(msg)
                    print(msg)

                except models.Scopus.DoesNotExist:
                    pass
        
        if doc.is_scopus == 0:
            try:
                docscopus = models.Scopus.objects.get(title_country__iexact = doc.title_country)
                doc.modify(
                    is_scopus = 1,
                    scopus_id = str(docscopus.id),
                    updated_at = datetime.datetime.now)
                doc.save() # save in WOS Collection

                msg = 'Title-Country WOS: %s is Scopus' % (doc.title_country)
                logger.info(msg)
                print(msg)

            except models.Scopus.DoesNotExist:
                pass

def stats():
    print('WoS total records: %s' % (models.Wos.objects.count()))
    print('WoS     is_scielo: %s' % (models.Wos.objects.filter(is_scielo = 1).count()))
    print('WoS    is_scimago: %s' % (models.Wos.objects.filter(is_scimago = 1).count()))
    print('WoS     is_scopus: %s' % (models.Wos.objects.filter(is_scopus = 1).count()))



def main():
    match_scielo()
    match_scimago()
    match_scopus()

    stats()

if __name__ == "__main__":
    main()