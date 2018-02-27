# coding: utf-8
'''
This script reads data from Scimago xlsx files to process and laod in MongoDB.
'''
import os
import sys
import models
import pyexcel
import keycorrection
import logging
from accent_remover import *
import datetime

PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename='logs/scimago_loader.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


def scimago_loader():
    filelist = [f for f in os.listdir('data/scimago/xlsx/inscielo') if '.xlsx' in f]
    filelist.sort()

    for f in filelist:

        year = f[-16:-12]
        region = f[8:-15]

        print('ini: ' + str(datetime.datetime.now()))
        print('%s %s %s' % (year, region, f))

        scimago_sheet = pyexcel.get_sheet(
            file_name='data/scimago/xlsx/inscielo/' + f,
            name_columns_by_row=0)

        # Key correction
        for i, k in enumerate(keycorrection.scimago_columns_names):
            scimago_sheet.colnames[i] = k

        scimago_json = scimago_sheet.to_records()

        for rec in scimago_json:

            issns = rec['issn'].replace('ISSN ', '').replace(' ', '').split(',')
            rec['issn_list'] = [i[0:4] + '-' + i[4:8] for i in issns]

            # check if exist in DB - update inSciELO
            flag = 0

            for issn in rec['issn_list']:

                query = models.Scimago.objects.filter(issn_list=issn)

                if len(query) == 1 and flag == 0:

                    data = {}
                    data['inscielo'] = 1

                    query[0].modify(**data)
                    query[0].save()

                    flag = 1
                    break

        msg = issn
        logger.info(msg)

        print(msg)

        print('fim:' + str(datetime.datetime.now()) + '\n')


def main():
    scimago_loader()

if __name__ == "__main__":
    main()
