# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import logging

import models

import pyexcel

logging.basicConfig(
    filename='logs/ga_scholar_manual.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


# Add metrics of Google Scholar for journals
def gscholar(filename):

    print(filename)

    gscholar = pyexcel.get_sheet(file_name=filename, sheet_name='import',
                                 name_columns_by_row=0)

    gscholar_json = gscholar.to_records()

    for rec in gscholar_json:
        # # remove empty keys
        # rec = {k: v for k, v in rec.items() if v or v == 0}
        query = models.Scielo.objects.filter(issn_list=rec['issn'])

        doc = query[0]

        data = {}
        data['google_scholar_h5_2017'] = rec['h5_2017']
        data['google_scholar_m5_2017'] = rec['m5_2017']
        data['google_scholar_h5_2018'] = rec['h5_2018']
        data['google_scholar_m5_2018'] = rec['m5_2018']

        if data:
            doc.modify(**data)


def main():
    # Google Scholar H5 M5
    # Indicators manually extracted
    gscholar('data/google/h5_m5_brasil_rcfapesp_2018.xlsx')

if __name__ == "__main__":
    main()
