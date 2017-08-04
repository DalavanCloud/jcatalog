# coding: utf-8
'''
This script get the country from others Data Sets and
saves in the CWTS collection.
'''
import logging

from accent_remover import *
import models

logging.basicConfig(
    filename='logs/match_wos_country.info.txt',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def match():

    for doc in models.Cwts.objects().batch_size(5):
        print(doc.issn_list)

        flag = 0

        for issn in doc.issn_list:
            for db in [models.Scielo, models.Scopus, models.Scimago]:

                query = db.objects.filter(issn_list=issn)

                if len(query) > 0 and flag == 0:

                    flag = 1

                    print(db._class_name)

                    data = get_country(query[0])

                    if data and 'country' in data:
                        data['title_country'] = '%s-%s' % (
                            accent_remover(doc.title).lower().replace(' & ', ' and ').replace('&', ' and '),
                            data['country'].lower())

                        print(data)

                        doc.modify(**data)
                        doc.save()

                        break


def get_country(query):

    if 'country' in query:
        country = query['country']
    else:
        country = None

    if country:
        data_modify = {'country': country}
    else:
        data_modify = None

    result = data_modify

    return result


def main():
    match()

if __name__ == "__main__":
    main()
