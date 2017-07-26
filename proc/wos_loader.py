# coding: utf-8
'''
This script reads data from JCR CSV files to process and laod in MongoDB.
'''
import os
import sys
import models
import pyexcel
import keycorrection
import logging
from accent_remover import *
import collections_wos


PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename='logs/wos_loader.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)

filelist = [f for f in os.listdir('data/wos/')]
filelist.sort()

models.Wos.drop_collection()

for f in filelist:

    print(f)

    year = f[20:-4]
    col = f[16:-9]

    print(col)
    print(year)

    country = collections_wos.country[col]

    wos_sheet = pyexcel.get_sheet(file_name='data/wos/' + f, name_columns_by_row=0)

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
        if len(rec['issn']) == 9:

            flag = 0

            rec['country'] = country

            rec['issn_list'] = [rec['issn']]

            rec['title_country'] = '%s-%s' % (
                accent_remover(rec['title']).lower(),
                rec['country'].lower())

            # remove empty keys
            rec = {k: v for k, v in rec.items() if v or v == 0}

            query = models.Wos.objects.filter(issn_list=rec['issn'])

            if len(query) == 0 and flag == 0:

                rec[str(year)] = {}

                for t, k in [
                        (int, 'total_cites'),
                        (float, 'journal_impact_factor'),
                        (float, 'impact_factor_without_journal_self_cites'),
                        (float, 'five_year_impact_factor'),
                        (float, 'immediacy_index'),
                        (int, 'citable_items'),
                        (str, 'cited_half_life'),
                        (str, 'citing_half_life'),
                        (float, 'eigenfactor_score'),
                        (float, 'article_influence_score'),
                        (float, 'percentage_articles_in_citable_items'),
                        (float, 'average_journal_impact_factor_percentile'),
                        (float, 'normalized_eigenfactor')
                        ]:

                    if k in rec:
                        if type(rec[k]) == str and ',' in rec[k]:
                            rec[str(year)][k] = int(rec[k].replace(',', ''))
                        elif type(rec[k]) == str and 'Not Available' in rec[k]:
                            rec[str(year)][k] = str(rec[k])
                        else:
                            rec[str(year)][k] = t(rec[k])

                        del rec[k]

                mdata = models.Wos(**rec)
                mdata.save()
                flag = 1

            if len(query) == 1 and flag == 0:

                data = {}
                data[str(year)] = {}

                for t, k in [
                        (int, 'total_cites'),
                        (float, 'journal_impact_factor'),
                        (float, 'impact_factor_without_journal_self_cites'),
                        (float, 'five_year_impact_factor'),
                        (float, 'immediacy_index'),
                        (int, 'citable_items'),
                        (str, 'cited_half_life'),
                        (str, 'citing_half_life'),
                        (float, 'eigenfactor_score'),
                        (float, 'article_influence_score'),
                        (float, 'percentage_articles_in_citable_items'),
                        (float, 'average_journal_impact_factor_percentile'),
                        (float, 'normalized_eigenfactor')
                        ]:

                    if k in rec:
                        if type(rec[k]) == str and ',' in rec[k]:
                            data[str(year)][k] = int(rec[k].replace(',', ''))
                        elif type(rec[k]) == str and 'Not Available' in rec[k]:
                            data[str(year)][k] = str(rec[k])
                        else:
                            data[str(year)][k] = t(rec[k])

                        del rec[k]

                    query[0].modify(**data)
                    query[0].save()
                    flag = 1

    num_posts = models.Wos.objects().count()
    msg = u'Registred %d posts in WOS collection' % num_posts
    logger.info(msg)
    print(msg)
