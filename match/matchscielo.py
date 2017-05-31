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

logging.basicConfig(filename='logs/matchscielo.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)

from proc import models


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

    docs = models.Scielo.objects()

    for doc in docs: # for each document in Scielo
        
        flag = 0
        
        if doc.is_wos == 0:  
            
            # 1) Try match for each ISSN from the issn_list
            for issn in doc.issn_list:

                if flag == 0:

                    query_issn_wos = models.Wos.objects.filter(issn_list=issn)

                    # 1.1) If query retured only 1 document (by ISSN)             
                    if len(query_issn_wos) == 1 and flag == 0:  
                        doc.modify(
                            is_wos=1,
                            wos_id=str(query_issn_wos[0].id),
                            updated_at=datetime.datetime.now)
                        doc.save()  # save in Scielo Collection

                        msg = 'ISSN Scielo: %s is Wos' % (issn)
                        logger.info(msg)
                        print(msg)
                        
                        flag = 1
                        
                        break

                    # 1.2) If query by ISSN returned more than 1 document, try query by ISSN and similar title
                    if len(query_issn_wos) > 1 and flag == 0:

                        query_issn_title_wos = models.Wos.objects.filter(issn_list=issn, full_journal_title__iexact=doc.title_at_scielo)

                        if len(query_issn_title_wos) == 1:
                            doc.modify(
                                is_wos=1,
                                wos_id=str(query_issn_title_wos[0].id),
                                updated_at=datetime.datetime.now)
                            doc.save()  # save in Scielo Collection

                            msg = 'ISSN and title Scielo: %s : %s is Wos' % (issn, doc.title_at_scielo)
                            logger.info(msg)
                            print(msg)
                            
                            flag = 1
                            
                            break

                        else:  # 1.2.1)If query by ISSN and similar title is 0 or more than 1, get the document with more indicators from query by ISSN (query_issn_scimago)
                            
                            knum = {}
                            
                            for i, d in enumerate(query_issn_wos):
                                knum[str(d.id)] = len([k for k in query_issn_wos[i]])

                            doc.modify(
                                is_wos=1,
                                wos_id=max(knum, key=knum.get),
                                updated_at=datetime.datetime.now)
                            doc.save()  # save in Scielo Collection

                            msg = 'ISSN Scielo: %s is Wos with %s fields)' % (issn, str(max(knum, key=knum.get)))
                            logger.info(msg)
                            print(msg)
                            
                            flag = 1
                            
                            break

            # 2) If flag is still zero, no match by ISSN. Try by similarity of title and country
            if flag == 0:

                query_title_pais_wos = models.Wos.objects.filter(title_country__iexact=doc.title_at_scielo_country)

                if len(query_title_pais_wos):
                    doc.modify(
                        is_wos=1,
                        wos_id=str(query_title_pais_wos[0].id),
                        updated_at=datetime.datetime.now)
                    doc.save()  # save in Scielo Collection

                    msg = 'Title and country Scielo: %s is Wos' % (doc.title_at_scielo_country)
                    logger.info(msg)
                    print(msg)
                    
                    flag = 1

            # 3) If flag is still zero, filter didn't find documents
            if flag == 0:

                msg = 'Not found in Wos %s : %s' % (doc.issn_list, doc.title_at_scielo)
                logger.info(msg)
                print(msg)
                
                pass

def match_scimago():

    docs = models.Scielo.objects()

    for doc in docs: # for each document in Scielo
        
        flag = 0
        
        if doc.is_scimago == 0:  
            
            # 1) Try match for each ISSN from the issn_list
            for issn in doc.issn_list:

                if flag == 0:

                    query_issn_scimago = models.Scimago.objects.filter(issn_list=issn)

                    # 1.1) If query retured only 1 document (by ISSN)             
                    if len(query_issn_scimago) == 1 and flag == 0:  
                        doc.modify(
                            is_scimago=1,
                            scimago_id=str(query_issn_scimago[0].id),
                            updated_at=datetime.datetime.now)
                        doc.save()  # save in Scielo Collection

                        msg = 'ISSN Scielo: %s is Scimago' % (issn)
                        logger.info(msg)
                        print(msg)
                        
                        flag = 1
                        
                        break

                    # 1.2) If query returned more than 1 document, try by ISSN and similar title
                    if len(query_issn_scimago) > 1 and flag == 0:

                        query_issn_title_scimago = models.Scimago.objects.filter(issn_list=issn, title__iexact=doc.title_at_scielo)

                        if len(query_issn_title_scimago) == 1:
                            doc.modify(
                                is_scimago=1,
                                scimago_id=str(query_issn_title_scimago[0].id),
                                updated_at=datetime.datetime.now)
                            doc.save()  # save in Scielo Collection

                            msg = 'ISSN and title Scielo: %s : %s is Scimago' % (issn, doc.source_title)
                            logger.info(msg)
                            print(msg)
                            
                            flag = 1
                            
                            break

                        else:  # 1.2.1) If query by ISSN and similar title is 0 or more than 1, get the document with more indicators from query by ISSN (query_issn_scimago)
                            
                            knum = {}

                            for i, d in enumerate(query_issn_scimago):
                                knum[str(d.id)] = len([k for k in query_issn_scimago[i]])

                            doc.modify(
                                is_scimago=1,
                                scimago_id=max(knum, key=knum.get),
                                updated_at=datetime.datetime.now)
                            doc.save()  # save in Scielo Collection

                            msg = 'ISSN Scielo: %s is Scimago with %s fields)' % (issn, str(max(knum, key=knum.get)))
                            logger.info(msg)
                            print(msg)
                            
                            flag = 1
                            
                            break

            # 2) If flag is still zero, no match by ISSN. Try by similarity of title and country
            if flag == 0:

                query_title_pais_scimago = models.Scimago.objects.filter(title_country__iexact=doc.title_at_scielo_country)

                if len(query_title_pais_scimago):
                    doc.modify(
                        is_scimago=1,
                        scimago_id=str(query_title_pais_scimago[0].id),
                        updated_at=datetime.datetime.now)
                    doc.save()  # save in Scielo Collection

                    msg = 'Title and country Scielo: %s is Scimago' % (doc.title_at_scielo_country)
                    logger.info(msg)
                    print(msg)
                    
                    flag = 1

            # 3) If flag is still zero, filter didn't find documents
            if flag == 0:

                msg = 'Not found in Scimago  %s : %s' % (doc.issn_list, doc.title_at_scielo)
                logger.info(msg)
                print(msg)
                
                pass


def match_scopus():

    docs = models.Scielo.objects()

    for doc in docs: # for each document in Scielo
        
        flag = 0
        
        if doc.is_scopus == 0:  
            
            # 1) Try match for each ISSN from the issn_list
            for issn in doc.issn_list:

                if flag == 0:

                    query_issn_scopus = models.Scopus.objects.filter(issn_list=issn)

                    # 1.1) If query retured only 1 document (by ISSN)             
                    if len(query_issn_scopus) == 1 and flag == 0:  
                        doc.modify(
                            is_scopus=1,
                            scopus_id=str(query_issn_scopus[0].id),
                            updated_at=datetime.datetime.now)
                        doc.save()  # save in Scielo Collection

                        msg = 'ISSN Scielo: %s is Scopus' % (issn)
                        logger.info(msg)
                        print(msg)
                        
                        flag = 1
                        
                        break

                    # 1.2) If query returned more than 1 document, try by ISSN and similar title
                    if len(query_issn_scopus) > 1 and flag == 0:

                        query_issn_title_scopus = models.Scopus.objects.filter(issn_list=issn, source_title__iexact=doc.title_at_scielo)

                        if len(query_issn_title_scopus) == 1:
                            doc.modify(
                                is_scopus=1,
                                scopus_id=str(query_issn_title_scopus[0].id),
                                updated_at=datetime.datetime.now)
                            doc.save()  # save in Scielo Collection

                            msg = 'ISSN and title Scielo: %s : %s is Scopus' % (issn, doc.source_title)
                            logger.info(msg)
                            print(msg)
                            
                            flag = 1
                            
                            break

                        else:  # 1.2.1) If query by ISSN and similar title is 0 or more than 1, get the document with more indicators from query by ISSN (query_issn_scopus)
                            
                            knum = {}

                            for i, d in enumerate(query_issn_scopus):
                                knum[str(d.id)] = len([k for k in query_issn_scopus[i]])

                            doc.modify(
                                is_scopus=1,
                                scopus_id=max(knum, key=knum.get),
                                updated_at=datetime.datetime.now)
                            doc.save()  # save in Scielo Collection

                            msg = 'ISSN Scielo: %s is Scopus with %s fields)' % (issn, str(max(knum, key=knum.get)))
                            logger.info(msg)
                            print(msg)
                            
                            flag = 1
                            
                            break

            # 2) If flag is still zero, no match by ISSN. Try by similarity of title and country
            if flag == 0:

                query_title_pais_scopus = models.Scopus.objects.filter(title_country__iexact=doc.title_at_scielo_country)

                if len(query_title_pais_scopus):
                    doc.modify(
                        is_scopus=1,
                        scopus_id=str(query_title_pais_scopus[0].id),
                        updated_at=datetime.datetime.now)
                    doc.save()  # save in Scielo Collection

                    msg = 'Title and country Scielo: %s is Scopus' % (doc.title_at_scielo_country)
                    logger.info(msg)
                    print(msg)
                    
                    flag = 1

            # 3) If flag is still zero, filter didn't find documents
            if flag == 0:

                msg = 'Not found in Scopus  %s : %s' % (doc.issn_list, doc.title_at_scielo)
                logger.info(msg)
                print(msg)
                
                pass


def stats():
    print('SciELO total records: %s' % (models.Scielo.objects.count()))
    print('SciELO    is_scimago: %s' % (models.Scielo.objects.filter(is_scimago = 1).count()))
    print('SciELO     is_scopus: %s' % (models.Scielo.objects.filter(is_scopus = 1).count()))
    print('SciELO        is_wos: %s' % (models.Scielo.objects.filter(is_wos = 1).count()))


def main():
    submissions()
    match_wos()
    match_scimago()
    match_scopus()

    stats()


if __name__ == "__main__":
    main()
