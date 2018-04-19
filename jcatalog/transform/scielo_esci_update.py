# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import pyexcel
import logging

from accent_remover import *
import models


logging.basicConfig(filename='logs/esci.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


def esci(filename):
    sheet = pyexcel.get_sheet(
        file_name=filename,
        sheet_name='import',
        name_columns_by_row=0)

    sheet_json = sheet.to_records()

    for rec in sheet_json:
        print(rec['issn'])

        data = None
        query = models.Scielo.objects.filter(issn_scielo=rec['issn'])

        if len(query) == 1:
            data = {'esci': 1}
        else:
            title_country = '%s-%s' % (accent_remover(rec['title']).lower().replace(' & ', ' and ').replace('&', ' and '), 'brazil')

            query = models.Scielo.objects.filter(title_country=title_country)
            if len(query) == 1:
                print(title_country)
                data = {'esci': 1}

        if data:
            query[0].modify(**data)


def main():
    esci('data/scielo/esci-html pages.xlsx')


if __name__ == "__main__":
    main()
