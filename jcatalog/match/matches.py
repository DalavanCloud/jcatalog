# coding: utf-8

'''
This script perform data matching between two journals Data Sets
of various sources.
'''
import logging
import datetime
from mongoengine import *
import models

logging.basicConfig(filename='logs/matches.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


def match(dbcol1, dbcol2, country=None):

    db1 = dbcol1._class_name
    db2 = dbcol2._class_name

    # DataSet2 - name of DB collection 2. e.g.: 'wos'
    col = dbcol2._class_name.lower()

    # for each document in dbcol1
    for doc in dbcol1.objects().batch_size(5):

        flag = 0

        # e.g.: if doc.is_scielo == 0
        if eval('doc.is_' + col + ' == 0'):

            # 1) Try match for each ISSN from the issn_list
            for issn in doc.issn_list:

                if flag == 0:

                    query_issn = ''

                    query_issn = dbcol2.objects.filter(issn_list=issn)

                    # 1.1) If query retured only 1 document (by ISSN)
                    if len(query_issn) == 1 and flag == 0:

                        countrycol = ''

                        if 'country' in query_issn[0]:
                            if country == 1:
                                countrycol = query_issn[0].country
                        else:
                            countrycol = None

                        data_modify = {
                            'is_' + col: 1,
                            col + '_id': str(query_issn[0].id),
                            'updated_at': datetime.datetime.now,
                            'country_' + col: countrycol}

                        doc.modify(**data_modify)
                        doc.save()  # save in dbcol1 collection

                        msg = '%s : ISSN %s is %s' % (db1, issn, db2)
                        logger.info(msg)
                        print(msg)
                        flag = 1

                        break

                    '''
                    1.2) If query returned more than 1 document, try by
                    ISSN and similar title
                    '''
                    if len(query_issn) > 1 and flag == 0:

                        query_issn_title = ''

                        query_issn_title = dbcol2.objects.filter(issn_list=issn, title__iexact=doc.title)

                        if len(query_issn_title) == 1:

                            countrycol = ''
                            if 'country' in query_issn[0]:
                                if country == 1:
                                    countrycol = query_issn[0].country
                            else:
                                countrycol = None

                            data_modify = {
                                'is_' + col: 1,
                                col + '_id': str(query_issn_title[0].id),
                                'updated_at': datetime.datetime.now,
                                'country_' + col: countrycol}
                            doc.modify(**data_modify)
                            doc.save()  # save in dbcol1 collection

                            msg = '%s : ISSN and title : %s : %s is %s' % (db1, issn, doc.title, db2)
                            logger.info(msg)
                            print(msg)

                            flag = 1

                            break

                        '''
                        1.2.1) If query by ISSN and similar title is 0 or more
                        than 1, get the document with more indicators from
                        query by ISSN (query_issn_scopus)
                        '''
                        if len(query_issn_title) > 1 and flag == 0:

                            knum = {}

                            for i, d in enumerate(query_issn):
                                knum[str(d.id)] = len([k for k in query_issn[i]])

                            countrycol = ''
                            if 'country' in query_issn[0]:
                                if country == 1:
                                    countrycol = query_issn[0].country
                            else:
                                countrycol = None

                                data_modify = {
                                    'is_' + col: 1,
                                    col + '_id': max(knum, key=knum.get),
                                    'updated_at': datetime.datetime.now,
                                    'country_' + col: countrycol}
                                doc.modify(**data_modify)
                                doc.save()  # save in dbcol1 collection

                            msg = '%s : ISSN %s is %s with %s fields)' % (db1, issn, db2, str(max(knum, key=knum.get)))
                            logger.info(msg)
                            print(msg)

                            flag = 1

                            break

            # 2) If flag is still zero, try by similarity of title and country
            if flag == 0:

                if 'title_country' in doc:
                    query_title_pais = dbcol2.objects.filter(title_country__iexact=doc.title_country)

                    if len(query_title_pais) > 0:

                        countrycol = ''
                        if 'country' in query_title_pais[0]:
                            if country == 1:
                                countrycol = query_title_pais[0].country
                            else:
                                countrycol = None

                        data_modify = {
                            'is_' + col: 1,
                            col + '_id': str(query_title_pais[0].id),
                            'updated_at': datetime.datetime.now,
                            'country_' + col: countrycol}
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
    '''
    match(DataSet1, DataSet2, country)
    contry = 1 to get country of DataSet2
    '''

    # SciELO
    match(models.Scielo, models.Wos, 1)
    match(models.Scielo, models.Scopus, 1)
    match(models.Scielo, models.Scimago, 1)
    match(models.Scielo, models.Cwts, 1)

    # WoS
    match(models.Wos, models.Scielo, 1)
    match(models.Wos, models.Scopus, 1)
    match(models.Wos, models.Scimago, 1)
    match(models.Wos, models.Cwts, 1)

    # Scopus
    match(models.Scopus, models.Wos, 1)
    match(models.Scopus, models.Scielo, 1)
    match(models.Scopus, models.Scimago, 1)

    # Scimago
    match(models.Scimago, models.Wos, 1)
    match(models.Scimago, models.Scielo, 1)
    match(models.Scimago, models.Scopus, 1)

    # CWTS
    match(models.Cwts, models.Wos, 1)
    match(models.Cwts, models.Scielo, 1)
    match(models.Cwts, models.Scopus, 1)

if __name__ == "__main__":
    main()
