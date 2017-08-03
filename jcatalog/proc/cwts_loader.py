# coding: utf-8
'''
This script reads data from CWTS xlsx files to process and laod in MongoDB.
'''
import os
import sys
import models
import pyexcel
import keycorrection
import logging
from accent_remover import *

PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename='logs/cwts_loader.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)

models.Cwts.drop_collection()

cwts_sheet = pyexcel.get_sheet(
    file_name='data/cwts/CWTS Journal Indicators June 2017.xlsx',
    name_columns_by_row=0)

# Key correction
for i, k in enumerate(keycorrection.cwts_columns_names):
    cwts_sheet.colnames[i] = k

cwts_json = cwts_sheet.to_records()

for rec in cwts_json:

    if rec['year']:
        year = rec['year']

    rec['issn_list'] = []

    if 'print_issn' in rec and len(rec['print_issn']) > 2:
        rec['issn_list'].append(rec['print_issn'])
        if rec['print_issn'] == '-':
            del rec['print_issn']

    if 'electronic_issn' in rec and len(rec['electronic_issn']) > 2:
        rec['issn_list'].append(rec['electronic_issn'])
        if rec['electronic_issn'] == '-':
            del rec['electronic_issn']

    # remove empty keys
    rec = {k: v for k, v in rec.items() if v or v == 0}

    # check if exist in DB - create or update
    flag = 0

    if 'issn_list' in rec:

        for issn in rec['issn_list']:

            query = models.Cwts.objects.filter(issn_list=issn)

            if len(query) == 0 and flag == 0:

                rec[str(year)] = {}

                for k in [
                    'asjc_field_ids',
                    'citing_source',
                    'p',
                    'ipp',
                    'ipp_lower_bound',
                    'ipp_upper_bound',
                    'snip',
                    'snip_lower_bound',
                    'snip_upper_bound',
                    'percentage_self_cit'
                ]:

                    if k in rec:
                        rec[str(year)][k] = rec[k]
                        del rec[k]

                mdata = models.Cwts(**rec)
                mdata.save()
                flag = 1
                break

            if len(query) == 1 and flag == 0:

                data = {}
                data[str(year)] = {}

                for k in [
                    'asjc_field_ids',
                    'citing_source',
                    'p',
                    'ipp',
                    'ipp_lower_bound',
                    'ipp_upper_bound',
                    'snip',
                    'snip_lower_bound',
                    'snip_upper_bound',
                    'percentage_self_cit'
                ]:

                    if k in rec:
                        data[str(year)][k] = rec[k]

                query[0].modify(**data)
                query[0].save()
                flag = 1
                break

        print('%s - %s' % (year, rec['issn_list']))

num_posts = models.Cwts.objects().count()
msg = u'Registred %d posts in CWTS collection' % num_posts
logger.info(msg)

print(msg)
