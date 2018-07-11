# coding: utf-8
'''
This script reads data from Scimago CSV files to process and laod in MongoDB.
'''
import os
import sys
import models
import keycorrection
import logging
from accent_remover import *
import datetime
import csv
import json

PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename='logs/scimago_loader.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


def scimago_loader():
    filelist = [f for f in os.listdir('data/scimago/csv') if '.csv' in f]
    filelist.sort()

    for f in filelist:

        year = f[-8:-4]
        region = f[8:-9]

        print('ini: ' + str(datetime.datetime.now()))
        print('%s %s %s' % (year, region, f))

        listfield = tuple(keycorrection.scimago_columns_names)
        exampleFile = open('data/scimago/csv/'+f)
        exampleReader = csv.DictReader(exampleFile, fieldnames=listfield, delimiter=';')
        out = json.dumps([row for row in exampleReader])
        scimago_json = json.loads(out)
        del scimago_json[0]

        for rec in scimago_json:

            rec['region'] = region.replace('_', ' ')

            rec['title_country'] = '%s-%s' % (
                accent_remover(rec['title']).lower(),
                rec['country'].lower()
                )

            issns = str(rec['issn']).replace('ISSN ', '').replace(' ', '').split(',')
            rec['issn_list'] = []
            for i in issns:
                if len(i) == 7:
                    rec['issn_list'].append(i[0:4] + '-' + i[4:8]+'X')
                else:
                    rec['issn_list'].append(i[0:4] + '-' + i[4:8])

            # remove empty keys
            rec = {k: v for k, v in rec.items() if v or v == 0}

            rec['updated_at'] = datetime.datetime.now()

            if 'rank' in rec:
                rec['rank'] = int(rec['rank'])
            if 'sourceid' in rec:
                rec['sourceid'] = int(rec['sourceid'])
            if 'sjr' in rec:
                rec['sjr'] = float(rec['sjr'].replace(',', '.'))
            rec['h_index'] = int(rec['h_index'])
            rec['total_docs'] = int(rec['total_docs'])
            rec['total_docs_3years'] = int(rec['total_docs_3years'])
            rec['total_refs'] = int(rec['total_refs'])
            rec['total_cites_3years'] = int(rec['total_cites_3years'])
            rec['citable_docs_3years'] = int(rec['citable_docs_3years'])
            rec['cites_by_doc_2years'] = float(rec['cites_by_doc_2years'].replace(',', '.'))
            rec['ref_by_doc'] = float(rec['ref_by_doc'].replace(',', '.'))

            # check if exist in DB - create or update
            flag = 0

            for issn in rec['issn_list']:

                query = models.Scimago.objects.filter(issn_list=issn)

                if len(query) == 0 and flag == 0:
                    print('new: '+region+'_'+year+'_'+rec['title_country'])

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
                        if k in rec:
                            # categories
                            if k == 'categories':
                                if 'categories' in rec:
                                    rec[str(year)]['categories_list'] = rec[k].split(';')
                                    del rec[k]
                            else:
                                rec[str(year)][k] = rec[k]
                                del rec[k]

                    mdata = models.Scimago(**rec)
                    mdata.save()
                    flag = 1
                    break

                if len(query) > 0 and flag == 0:
                    for q in query:
                        print('old: '+region+'_'+year+'_'+rec['title_country'])

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
                            if k in rec:
                                # categories
                                if k == 'categories':
                                    if 'categories' in rec:
                                        data[str(year)]['categories_list'] = rec[k].split(';')
                                        del rec[k]
                                else:
                                    if k in rec:
                                        data[str(year)][k] = rec[k]
                                        del rec[k]
                        data['revis'] = 1
                        # doc = query[0]
                        q.modify(**data)
                        # query[0].save()
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