# coding: utf-8
'''
This script reads data from OECD xlsx file to process and laod in MongoDB.
'''
import logging
import pyexcel

import models

logging.basicConfig(filename='logs/oecd_loader.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)

models.Oecd.drop_collection()

oecd_sheet = pyexcel.get_sheet(
    file_name='data/oecd/oecd_category_mapping_2012.xlsx',
    name_columns_by_row=0)

# Key correction
for i, l in enumerate(oecd_sheet.colnames):
    oecd_sheet.colnames[i] = l.lower()

oecd_json = oecd_sheet.to_records()

for rec in oecd_json:

    rec['oecd_code'] = []
    rec['oecd_code'].append(rec['description'].split(' ', 1)[0])

    rec['oecd_description'] = []
    rec['oecd_description'].append(rec['description'].split(' ', 1)[1])

    del rec['description']

    # check if exist in DB - create or update
    query = models.Oecd.objects.filter(wos_description=rec['wos_description'])

    if len(query) == 0:

        mdata = models.Oecd(**rec)
        mdata.save()

    if len(query) == 1:
        if rec['oecd_description'][0] not in query[0]['oecd_description']:
            data = {}
            data['oecd_code'] = []
            data['oecd_description'] = []

            for d in query[0]['oecd_code']:
                data['oecd_code'].append(d)

            data['oecd_code'].append(rec['oecd_code'][0])

            for d in query[0]['oecd_description']:
                data['oecd_description'].append(d)

            data['oecd_description'].append(rec['oecd_description'][0])

        query[0].modify(**data)
        query[0].save()

num_posts = models.Oecd.objects().count()
msg = u'Registred %d posts in OECD collection' % num_posts
logger.info(msg)

print(msg)
