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

logging.basicConfig(filename='logs/matchwos.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)

from proc import models


def match_scielo():

    docs = models.Wos.objects().batch_size(5)

    for doc in docs: # for each document in Wos
        
        flag = 0
        
        if doc.is_scielo == 0:
            
            # 1) Try match for each ISSN from the issn_list
            for issn in doc.issn_list:

                if flag == 0:

                    query_issn_scielo = models.Scielo.objects.filter(issn_list=issn)

                    # 1.1) If query retured only 1 document (by ISSN)
                    if len(query_issn_scielo) == 1 and flag == 0:
                        doc.modify(
                            is_scielo=1,
                            scielo_id=str(query_issn_scielo[0].id),
                            updated_at=datetime.datetime.now)
                        doc.save()  # save in Wos Collection

                        msg = 'ISSN Wos: %s is Scielo' % (issn)
                        logger.info(msg)
                        print(msg)
                        
                        flag = 1
                        
                        break

                    # 1.2) If query by ISSN returned more than 1 document, try query by ISSN and similar title
                    if len(query_issn_scielo) > 1 and flag == 0:

                        query_issn_title_scielo = models.Scielo.objects.filter(issn_list=issn, title__iexact=doc.title)

                        if len(query_issn_title_scielo) == 1:
                            doc.modify(
                                is_scielo=1,
                                scielo_id=str(query_issn_title_scielo[0].id),
                                updated_at=datetime.datetime.now)
                            doc.save()  # save in Wos Collection

                            msg = 'ISSN and title Wos: %s : %s is Scielo' % (issn, doc.title)
                            logger.info(msg)
                            print(msg)
                            
                            flag = 1
                            
                            break

                        else:  # 1.2.1)If query by ISSN and similar title is 0 or more than 1, get the document with more indicators from query by ISSN (query_issn_scimago)
                            
                            knum = {}
                            
                            for i, d in enumerate(query_issn_scielo):
                                knum[str(d.id)] = len([k for k in query_issn_scielo[i]])

                            doc.modify(
                                is_scielo=1,
                                scielo_id=max(knum, key=knum.get),
                                updated_at=datetime.datetime.now)
                            doc.save()  # save in Wos Collection

                            msg = 'ISSN Wos: %s is Scielo with %s fields)' % (issn, str(max(knum, key=knum.get)))
                            logger.info(msg)
                            print(msg)
                            
                            flag = 1
                            
                            break

            # 2) If flag is still zero, no match by ISSN. Try by similarity of title and country
            if flag == 0:

                query_title_pais_scielo = models.Scielo.objects.filter(title_country__iexact=doc.title_country)

                if len(query_title_pais_scielo) == 1:
                    doc.modify(
                        is_scielo=1,
                        scielo_id=str(query_title_pais_scielo[0].id),
                        updated_at=datetime.datetime.now)
                    doc.save()  # save in Wos Collection

                    msg = 'Title and country Wos: %s is Scielo' % (doc.title_country)
                    logger.info(msg)
                    print(msg)
                    
                    flag = 1

            # 3) If flag is still zero, filter didn't find documents
            if flag == 0:

                msg = 'Not found in Scielo %s : %s' % (doc.issn_list, doc.title)
                logger.info(msg)
                print(msg)
                
                pass


def match_scimago():

    docs = models.Wos.objects()

    for doc in docs: # for each document in Wos
        
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
                        doc.save()  # save in Wos Collection

                        msg = 'ISSN Wos: %s is Scimago' % (issn)
                        logger.info(msg)
                        print(msg)
                        
                        flag = 1
                        
                        break

                    # 1.2) If query returned more than 1 document, try by ISSN and similar title
                    if len(query_issn_scimago) > 1 and flag == 0:

                        query_issn_title_scimago = models.Scimago.objects.filter(issn_list=issn, title__iexact=doc.title)

                        if len(query_issn_title_scimago) == 1:
                            doc.modify(
                                is_scimago=1,
                                scimago_id=str(query_issn_title_scimago[0].id),
                                updated_at=datetime.datetime.now)
                            doc.save()  # save in Wos Collection

                            msg = 'ISSN and title Wos: %s : %s is Scimago' % (issn, doc.title)
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
                            doc.save()  # save in Wos Collection

                            msg = 'ISSN Wos: %s is Scimago with %s fields)' % (issn, str(max(knum, key=knum.get)))
                            logger.info(msg)
                            print(msg)
                            
                            flag = 1
                            
                            break

            # 2) If flag is still zero, no match by ISSN. Try by similarity of title and country
            if flag == 0:

                query_title_pais_scimago = models.Scimago.objects.filter(title_country__iexact=doc.title_country)

                if len(query_title_pais_scimago) == 1:
                    doc.modify(
                        is_scimago=1,
                        scimago_id=str(query_title_pais_scimago[0].id),
                        updated_at=datetime.datetime.now)
                    doc.save()  # save in Wos Collection

                    msg = 'Title and country Wos: %s is Scimago' % (doc.title_country)
                    logger.info(msg)
                    print(msg)
                    
                    flag = 1

            # 3) If flag is still zero, filter didn't find documents
            if flag == 0:

                msg = 'Not found in Scimago  %s : %s' % (doc.issn_list, doc.title)
                logger.info(msg)
                print(msg)
                
                pass


def match_scopus():

    docs = models.Wos.objects().batch_size(5)

    for doc in docs: # for each document in Wos
        
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
                        doc.save()  # save in Wos Collection

                        msg = 'ISSN Scimago: %s is Scopus' % (issn)
                        logger.info(msg)
                        print(msg)
                        
                        flag = 1
                        
                        break

                    # 1.2) If query returned more than 1 document, try by ISSN and similar title
                    if len(query_issn_scopus) > 1 and flag == 0:

                        query_issn_title_scopus = models.Scopus.objects.filter(issn_list=issn, title__iexact=doc.title)

                        if len(query_issn_title_scopus) == 1:
                            doc.modify(
                                is_scopus=1,
                                scopus_id=str(query_issn_title_scopus[0].id),
                                updated_at=datetime.datetime.now)
                            doc.save()  # save in Wos Collection

                            msg = 'ISSN and title Scimago: %s : %s is Scopus' % (issn, doc.title)
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
                            doc.save()  # save in Wos Collection

                            msg = 'ISSN Scimago: %s is Scopus with %s fields)' % (issn, str(max(knum, key=knum.get)))
                            logger.info(msg)
                            print(msg)
                            
                            flag = 1
                            
                            break

            # 2) If flag is still zero, no match by ISSN. Try by similarity of title and country
            if flag == 0:

                query_title_pais_scopus = models.Scopus.objects.filter(title_country__iexact=doc.title_country)

                if len(query_title_pais_scopus) == 1:
                    doc.modify(
                        is_scopus=1,
                        scopus_id=str(query_title_pais_scopus[0].id),
                        updated_at=datetime.datetime.now)
                    doc.save()  # save in Wos Collection

                    msg = 'Title and country Scimago: %s is Scopus' % (doc.title_country)
                    logger.info(msg)
                    print(msg)
                    
                    flag = 1

            # 3) If flag is still zero, filter didn't find documents
            if flag == 0:

                msg = 'Not found in Scopus  %s : %s' % (doc.issn_list, doc.title)
                logger.info(msg)
                print(msg)
                
                pass


def stats():
    print('WoS total records: %s' % (models.Wos.objects.count()))
    print('WoS     is_scielo: %s' % (models.Wos.objects.filter(is_scielo=1).count()))
    print('WoS    is_scimago: %s' % (models.Wos.objects.filter(is_scimago=1).count()))
    print('WoS     is_scopus: %s' % (models.Wos.objects.filter(is_scopus=1).count()))



def main():
    match_scielo()
    match_scimago()
    match_scopus()

    stats()

if __name__ == "__main__":
    main()