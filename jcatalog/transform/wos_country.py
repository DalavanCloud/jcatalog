# coding: utf-8
'''
This script get the country from others Data Sets and
saves in the Wos collection.
'''

import logging
import pyexcel

from accent_remover import *
import models

logging.basicConfig(
    filename='logs/wos_tecountry.info.txt',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def thematic_areas():
    sheet = pyexcel.get_sheet(
        file_name='data/wos/jcr_areas/WoS_2016.xlsx',
        sheet_name='journals',
        name_columns_by_row=0)

    wos_json = sheet.to_records()

    for j in wos_json:
        print(j['title'])

        query = models.Wos.objects.filter(title__iexact=j['title'])

        if query:

            for doc in query:

                data = {}

                # Thematic areas
                if 'thematic_areas' not in doc:
                    print('issn: ' + doc['issn'])
                    data['thematic_areas'] = j['category'].split(',')

                # Country and title_country
                if 'country' not in doc:
                    print('coun: ' + j['country'])

                    data['country'] = j['country'].title()

                    data['title_country'] = '%s-%s' % (
                    accent_remover(doc.title).lower().replace(' & ', ' and ').replace('&', ' and '),
                    data['country'].lower())

                # Publisher
                if 'publisher' not in doc:
                    print('publ: ' + j['publisher'])

                    data['publisher'] = j['publisher']

                # save
                if data:
                    doc.modify(**data)
                    doc.save()


def country():

    for doc in models.Wos.objects().batch_size(5):

        if 'country' not in doc:
            print(doc.issn_list)
            '''
            # Wos_scielo = 1a carga de WoS de paises da rede SciELO
            '''
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

    data_modify = {'country': country}

    result = data_modify

    return result


def main():

    thematic_areas()
    country()

if __name__ == "__main__":
    main()
