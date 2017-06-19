# coding: utf-8

'''
This script perform data matching between two journals Data Sets of various sources.
'''

import os
import sys
import logging
import datetime

from mongoengine import *


PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename='logs/matches.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


from proc import models


def match(dbcol1, dbcol2):

    db1 = dbcol1._class_name
    db2 = dbcol2._class_name

    col = dbcol2._class_name.lower() # DataSet2 - name of DB collection 2. e.g.: 'wos'

    for doc in dbcol1.objects().batch_size(5): # for each document in dbcol1
        
        flag = 0

        if eval('doc.is_' + col + ' == 0'): # e.g.: if doc.is_scielo == 0
            
            # 1) Try match for each ISSN from the issn_list
            for issn in doc.issn_list:

                if flag == 0:

                    query_issn = dbcol2.objects.filter(issn_list=issn)

                    # 1.1) If query retured only 1 document (by ISSN)             
                    if len(query_issn) == 1 and flag == 0:
                        
                        data_modify = {
                            'is_' + col : 1,
                            col + '_id' : str(query_issn[0].id),
                            'updated_at': datetime.datetime.now}
                        
                        doc.modify(**data_modify)
                        doc.save()  # save in dbcol1 collection

                        msg = '%s : ISSN %s is %s' % (db1, issn, db2)
                        logger.info(msg)
                        print(msg)
                        
                        flag = 1
                        
                        break

                    # 1.2) If query returned more than 1 document, try by ISSN and similar title
                    if len(query_issn) > 1 and flag == 0:

                        query_issn_title = dbcol2.objects.filter(issn_list=issn, title__iexact=doc.title)

                        if len(query_issn_title) == 1:

                            data_modify = {
                                'is_' + col : 1,
                                col + '_id' : str(query_issn_title[0].id),
                                'updated_at': datetime.datetime.now}
                            doc.modify(**data_modify)
                            doc.save()  # save in dbcol1 collection

                            msg = '%s : ISSN and title : %s : %s is %s' % (db1, issn, doc.title, db2)
                            logger.info(msg)
                            print(msg)
                            
                            flag = 1
                            
                            break

                        else:  # 1.2.1) If query by ISSN and similar title is 0 or more than 1, get the document with more indicators from query by ISSN (query_issn_scopus)
                            
                            knum = {}

                            for i, d in enumerate(query_issn):
                                knum[str(d.id)] = len([k for k in query_issn[i]])

                                data_modify = {
                                    'is_' + col : 1,
                                    col + '_id' : max(knum, key=knum.get),
                                    'updated_at': datetime.datetime.now}
                                doc.modify(**data_modify)
                                doc.save()  # save in dbcol1 collection

                            msg = '%s : ISSN %s is %s with %s fields)' % (db1, issn, db2, str(max(knum, key=knum.get)))
                            logger.info(msg)
                            print(msg)
                            
                            flag = 1
                            
                            break

            # 2) If flag is still zero, no match by ISSN. Try by similarity of title and country
            if flag == 0:

                query_title_pais = dbcol2.objects.filter(title_country__iexact=doc.title_country)

                if len(query_title_pais) == 1: #

                    data_modify = {
                        'is_' + col : 1,
                        col + '_id' : str(query_title_pais[0].id),
                        'updated_at': datetime.datetime.now}
                    doc.modify(**data_modify)
                    doc.save()  # save in dbcol1 collection

                    msg = '%s : title and country : %s is %s' % (db1, doc.title_country, db2)
                    logger.info(msg)
                    print(msg)

                    flag = 1


            # 3) If flag is still zero, filter didn't find documents
            if flag == 0:

                msg = '%s : %s  %s : not found' % (db1, doc.issn_list, doc.title)
                logger.info(msg)
                print(msg)

                pass


def main():
    # dbcol1 = DataSet1 - name of DB collection 1
    # dbcol2 = DataSet2 - name of DB collection 2
    # match(DataSet1, DataSet2)


    #SciELO
    dbcol1 = models.Scielo
    
    dbcol2 = models.Wos
    match(dbcol1, dbcol2)

    dbcol2 = models.Scopus
    match(dbcol1, dbcol2)

    dbcol2 = models.Scimago
    match(dbcol1, dbcol2)


    # WoS
    dbcol1 = models.Wos
    
    dbcol2 = models.Scielo
    match(dbcol1, dbcol2)

    dbcol2 = models.Scopus
    match(dbcol1, dbcol2)

    dbcol2 = models.Scimago
    match(dbcol1, dbcol2)


    # Scopus
    dbcol1 = models.Scopus
    
    dbcol2 = models.Wos
    match(dbcol1, dbcol2)

    dbcol2 = models.Scielo
    match(dbcol1, dbcol2)

    dbcol2 = models.Scimago
    match(dbcol1, dbcol2)


    # Scimago
    dbcol1 = models.Scimago
    
    dbcol2 = models.Wos
    match(dbcol1, dbcol2)

    dbcol2 = models.Scielo
    match(dbcol1, dbcol2)

    dbcol2 = models.Scopus
    match(dbcol1, dbcol2)


if __name__ == "__main__":
    main()
