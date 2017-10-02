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

    rec['oecd'] = []

    rec['oecd'].append({
        'code': rec['description'].split(' ', 1)[0],
        'description': rec['description'].split(' ', 1)[1]
            })

    del rec['description']

    # check if exist in DB - create or update
    query = models.Oecd.objects.filter(wos_description=rec['wos_description'])

    if len(query) == 0:

        mdata = models.Oecd(**rec)
        mdata.save()

    if len(query) == 1:

        data = {}
        data['oecd'] = []

        for d in query[0]['oecd']:
            if rec['oecd'][0] not in query[0]['oecd']:
                data['oecd'].append(d)
        data['oecd'].append(rec['oecd'][0])

        query[0].modify(**data)
        query[0].save()

num_posts = models.Oecd.objects().count()
msg = u'Registred %d posts in OECD collection' % num_posts
logger.info(msg)

print(msg)
