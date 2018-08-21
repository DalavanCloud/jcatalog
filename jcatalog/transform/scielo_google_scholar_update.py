# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import glob
import logging

import models

import pyexcel

logging.basicConfig(filename='logs/ga_access.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


# Add metrics of Google Scholar for journals
def gscholar(filename, year):

    print(filename)

    gscholar = pyexcel.get_sheet(
        file_name=filename,
        name_columns_by_row=0)

    # Edit labels

    labels = []

    for h in gscholar.colnames:
        labels.append(h.strip().lower())

    for i, k in enumerate(labels):
        gscholar.colnames[i] = k

    gscholar_json = gscholar.to_records()

    for rec in gscholar_json:
        # # remove empty keys
        # rec = {k: v for k, v in rec.items() if v or v == 0}

        # convert ISSN in list
        if 'issn' in rec:
            rec['issn_list'] = rec['issn'].split(',')
            rec['issn_list'] = [i.upper() for i in rec['issn_list']]

        # remove issn original field
        del rec['issn']

        flag = 0

        for issn in rec['issn_list']:

            query = models.Scielo.objects.filter(issn_list=issn)

            if len(query) == 1 and flag == 0:

                print("find: " + issn)

                doc = query[0]

                data = {}
                data['google_scholar_h5_' + year] = rec['h5-index']
                data['google_scholar_m5_' + year] = rec['h5-median']

                if data:
                    doc.modify(**data)

                flag = 1
                break

        if flag == 0:
            print('\nVerificar: ' + rec['title'] + ' | ' + issn)


def main():
    # Google Scholar H5 M5
    # Files sends by Anurag Acharya and Abel Packer in 2018-08-21
    list_file = glob.glob('data/google/scholar/' + '*csv')
    if list_file == []:
        print('\nNão há arquivos para carregar')
    else:
        for f in list_file:
            gscholar(f, '2018')
    # gscholar('data/google/scholar/www.scielo.br.csv', '2018')

if __name__ == "__main__":
    main()
