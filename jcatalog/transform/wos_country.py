# coding: utf-8
'''
This script get the country from others Data Sets and
saves in the Wos collection.
'''
import logging

from accent_remover import *
import models

logging.basicConfig(
    filename='logs/match_wos_country.info.txt',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def match():

    for doc in models.Wos.objects().batch_size(5):
        print(doc.issn)

        for db in [models.Wos_scielo, models.Scielo, models.Scopus, models.Scimago]:

            query = db.objects.filter(issn_list=doc.issn)

            if len(query) > 0:

                print(db._class_name)

                data = get_country(query[0])

                data['title_country'] = '%s-%s' % (
                    accent_remover(doc.title).lower().replace(' & ', ' and ').replace('&', ' and '),
                    data['country'].lower())

                print(data)

                doc.modify(**data)
                doc.save()  # save in dbcol1 collection

                break


def get_country(query):

    if 'country' in query:
        country = query['country']
    else:
        country = query['publishers_country']

    data_modify = {'country': country}

    result = data_modify

    return result


def main():
    match()

if __name__ == "__main__":
    main()
