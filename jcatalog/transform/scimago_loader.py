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
    filelist = [f for f in os.listdir('data/scimago/xlsx') if '.xlsx' in f]
    filelist.sort()

    models.Scimago.drop_collection()

    for f in filelist:

        year = f[-9:-5]
        region = f[8:-10]

        print('ini: ' + str(datetime.datetime.now()))
        print('%s %s %s' % (year, region, f))

        scimago_sheet = pyexcel.get_sheet(
            file_name='data/scimago/xlsx/' + f,
            name_columns_by_row=0)

        # Key correction
        for i, k in enumerate(keycorrection.scimago_columns_names):
            scimago_sheet.colnames[i] = k

        scimago_json = scimago_sheet.to_records()

        for rec in scimago_json:

            rec['region'] = region.replace('_', ' ')

            rec['title_country'] = '%s-%s' % (
                accent_remover(rec['title']).lower(),
                rec['country'].lower()
                )

            issns = rec['issn'].replace('ISSN ', '').replace(' ', '').split(',')
            rec['issn_list'] = [i[0:4] + '-' + i[4:8] for i in issns]

            # remove empty keys
            rec = {k: v for k, v in rec.items() if v or v == 0}

            # check if exist in DB - create or update
            flag = 0

            for issn in rec['issn_list']:

                query = models.Scimago.objects.filter(issn_list=issn)

                if len(query) == 0 and flag == 0:

                    rec[str(year)] = {}

                    for k in [
                        'rank',
                        'sjr',
                        'sjr_best_quartile',
                        'h_index',
                        'total_docs',
                        'total_docs_3years',
                        'total_refs',
                        'total_cites_3years',
                        'citable_docs_3years',
                        'cites_by_doc_2years',
                        'ref_by_doc',
                        'categories'
                            ]:

                        # categories
                        if k == 'categories':
                            rec[str(year)]['categories_list'] = rec[k].split(';')
                            del rec[k]
                        else:
                            rec[str(year)][k] = rec[k]
                            del rec[k]

                    mdata = models.Scimago(**rec)
                    mdata.save()
                    flag = 1
                    break

                if len(query) == 1 and flag == 0:

                    data = {}
                    data[str(year)] = {}

                    for k in [
                        'rank',
                        'sjr',
                        'sjr_best_quartile',
                        'h_index',
                        'total_docs',
                        'total_docs_3years',
                        'total_refs',
                        'total_cites_3years',
                        'citable_docs_3years',
                        'cites_by_doc_2years',
                        'ref_by_doc',
                        'categories'
                            ]:

                        # categories
                        if k == 'categories':
                            data[str(year)]['categories_list'] = rec[k].split(';')
                            del rec[k]
                        else:
                            if k in rec:
                                data[str(year)][k] = rec[k]
                                del rec[k]

                    query[0].modify(**data)
                    query[0].save()
                    flag = 1
                    break

        num_posts = models.Scimago.objects().count()
        msg = u'Registred %d posts in Scimago collection' % num_posts
        logger.info(msg)

        print(msg)

        print('fim:' + str(datetime.datetime.now()) + '\n')


def main():
    scimago_loader()

if __name__ == "__main__":
    main()
