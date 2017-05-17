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

logging.basicConfig(filename = 'logs/matchscielo.info.txt',level = logging.INFO)
logger = logging.getLogger(__name__)

from proc import models

# SCIELO
def submissions(): # Adds submissions data in the SciELO collection
    for doc in models.Submissions.objects():
        for issn in doc.issn_list:
            try:
                docsci = models.Scielo.objects.get(issn_list = issn)
                docsci.modify(
                    scholarone = doc.scholarone,
                    ojs_scielo = doc.ojs_scielo,
                    ojs_outro = doc.ojs_outro,
                    outro = doc.outro,
                    submission_access = doc.endereco_acesso,
                    updated_at = datetime.datetime.now)
                docsci.save() # save in SciELO Collection

                msg = 'ISSN: %s has Submission' % (issn)
                logger.info(msg)
                print(msg)

            except models.Scielo.DoesNotExist:
                pass


def match_wos(): 
    for doc in models.Scielo.objects(): # read WOS data
        if doc.is_wos == 0:
            for issn in doc.issn_list:
                try:
                    docwos = models.Wos.objects.get(issn_list = issn)
                    doc.modify(
                        is_wos = 1,
                        wos_id = str(docwos.id),
                        updated_at = datetime.datetime.now)
                    doc.save() # save in SciELO Collection

                    msg = 'ISSN WOS: %s is SciELO' % (issn)
                    logger.info(msg)
                    print(msg)

                except models.Wos.DoesNotExist:
                    pass

        if doc.is_wos == 0:
            try:
                docwos = models.Wos.objects.get(title_country__iexact = doc.title_at_scielo_country)
                doc.modify(
                    is_wos = 1,
                    wos_id = str(docwos.id),
                    updated_at = datetime.datetime.now)
                doc.save() # save in SciELO Collection

                msg = 'Title-Country SciELO: %s is WOS' % (docwos.title_country)
                logger.info(msg)
                print(msg)

            except models.Wos.DoesNotExist:
               pass


def match_scimago():
    for doc in models.Scielo.objects():
        if doc.is_scimago == 0:
            for issn in doc.issn_list:
                try:
                    docmago = models.Scimago.objects.get(issn_list = issn)
                    doc.modify(
                        is_scimago = 1,
                        scimago_id = str(docmago.id),
                        updated_at = datetime.datetime.now)
                    doc.save() # save in SciELO Collection

                    msg = 'ISSN SciELO: %s is Scimago' % (issn)
                    logger.info(msg)
                    print(msg)

                except models.Scimago.DoesNotExist:
                    pass

        if doc.is_scimago == 0:
            try:
                docmago = models.Scimago.objects.get(title_country__iexact = doc.title_at_scielo_country)
                doc.modify(
                    is_scimago = 1,
                    scimago_id = str(docmago.id),
                    updated_at = datetime.datetime.now)
                doc.save() # save in SciELO Collection

                msg = 'Title-Country SciELO: %s is Scimago' % (docmago.title_country)
                logger.info(msg)
                print(msg)

            except models.Scimago.DoesNotExist:
                pass


def match_scopus():
    for doc in models.Scielo.objects():
        if doc.is_scopus == 0:
            for issn in doc.issn_list:
                try:
                    docscopus = models.Scopus.objects.get(issn_list = issn)
                    doc.modify(
                        is_scopus = 1,
                        scopus_id = str(docscopus.id),
                        updated_at = datetime.datetime.now)
                    doc.save() # save in SciELO Collection

                    msg = 'ISSN SciELO: %s is Scopus' % (issn)
                    logger.info(msg)
                    print(msg)

                except models.Scopus.DoesNotExist:
                    pass
        
        if doc.is_scopus == 0:
            try:
                docscopus = models.Scopus.objects.get(title_country__iexact = doc.title_at_scielo_country)
                doc.modify(
                    is_scopus = 1,
                    scopus_id = str(docscopus.id),
                    updated_at = datetime.datetime.now)
                doc.save() # save in SciELO Collection

                msg = 'Title-Country SciELO: %s is Scopus' % (docscopus.title_country)
                logger.info(msg)
                print(msg)

            except models.Scopus.DoesNotExist:
                pass


def stats():
    print('SciELO total records: %s' % (models.Scielo.objects.count()))
    print('SciELO    is_scimago: %s' % (models.Scielo.objects.filter(is_scimago = 1).count()))
    print('SciELO     is_scopus: %s' % (models.Scielo.objects.filter(is_scopus = 1).count()))
    print('SciELO        is_wos: %s' % (models.Scielo.objects.filter(is_wos = 1).count()))


def main():
    submissions()
    # match_wos()
    # match_scimago()
    # match_scopus()

    stats()

if __name__ == "__main__":
    main()
