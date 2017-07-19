# coding: utf-8
'''
This script reads data from Wos xlsx files to process and laod in MongoDB.
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

logging.basicConfig(filename='logs/wos_loader.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)

filelist = [f for f in os.listdir('data/wos_update/')]
filelist.sort()

models.Wos.drop_collection()

for f in filelist:

    print(f)

    wos_sheet = pyexcel.get_sheet(
        file_name='data/wos_update/' + f,
        name_columns_by_row=0)

    # Key correction
    for i, k in enumerate(keycorrection.wos_columns_names):
        wos_sheet.colnames[i] = k

    wos_json_dup = wos_sheet.to_records()

    # remove duplicates
    wos_json = []

    for rec in wos_json_dup:

        if rec not in wos_json:

            wos_json.append(rec)

    for rec in wos_json:

        rec['issn_list'] = [rec['issn']]

        rec['title_country'] = '%s-%s' % (
            accent_remover(rec['title']).lower(),
            rec['country'].lower())

        # remove empty keys
        rec = {k: v for k, v in rec.items() if v or v == 0}

        mdata = models.Wos(**rec)
        mdata.save()

    num_posts = models.Wos.objects().count()
    msg = u'Registred %d posts in WOS collection' % num_posts
    logger.info(msg)
    print(msg)
