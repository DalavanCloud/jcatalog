# coding: utf-8
'''
This script get the thematic areas(category) from a worksheet,
country and publisher from other sources and saves in the Wos collection.
'''
from accent_remover import *
import models

import logging
import pyexcel


logging.basicConfig(
    filename='logs/wos_tecountry.info.txt',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def thematic_areas():
    sheet = pyexcel.get_sheet(
        file_name='data/wos/wos_country_publisher_category_2016.xlsx',
        sheet_name='journals',
        name_columns_by_row=0)

    wos_json = sheet.to_records()

    for j in wos_json:
        print(j['title'])

        query = None
        query = models.Wos.objects.filter(title__iexact=j['title'])

        if query:

            for doc in query:

                data = {}

                # Thematic areas
                if not hasattr(doc, 'thematic_areas'):
                    print('nao tem thematic')
                    data['thematic_areas'] = [j['category']]
                else:
                    data['thematic_areas'] = []
                    data['thematic_areas'] = doc['thematic_areas']
                    data['thematic_areas'].append(j['category'])

                # Country and title_country
                if 'country' not in doc:
                    data['country'] = j['country']
                    data['title_country'] = '%s-%s' % (
                    accent_remover(doc.title).lower().replace(' & ', ' and ').replace('&', ' and '),
                    data['country'].lower())

                # Publisher
                if 'publisher' not in doc:
                    data['publisher'] = j['publisher']

                # save
                if data:
                    doc.modify(**data)
                    doc.save()


def country():

    for doc in models.Wos.objects().batch_size(5):

        if 'country' not in doc:
            print(doc.issn_list)

            for db in [models.Scielo, models.Scopus, models.Scimago]:

                query = None
                query = db.objects.filter(issn_list=doc.issn)

                if query:

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

    data_modify = {}

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
