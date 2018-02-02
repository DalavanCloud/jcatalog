# coding: utf-8
'''
This script reads data from JCR CSV files to process and laod in MongoDB.
'''
import os
import logging
import pyexcel

import models
import keycorrection
from accent_remover import *


logging.basicConfig(filename='logs/wos_loader_all.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)

filelist = [f for f in os.listdir('data/wos/jcr_all/')]
filelist.sort()

# models.Wos.drop_collection()

for f in filelist:

    print(f)

    year = f[9:13]
    edition = f[4:8]

    print('%s - %s' % (edition, year))

    wos_sheet = pyexcel.get_sheet(file_name='data/wos/jcr_all/' + f, name_columns_by_row=0)

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
        # not to read the last lines
        if len(rec['issn']) == 9:

            flag = 0

            # remove empty keys
            rec = {k: v for k, v in rec.items() if v or v == 0}

            query = models.Wos.objects.filter(title__iexact=rec['title'])

            if len(query) == 0:

                print('new - '+rec['title'])

                rec['issn_list'] = [rec['issn']]

                rec['citation_database'] = []
                rec['citation_database'].append(edition)

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

            if len(query) > 0:

                print('old - '+rec['title'])

                data = {}

                for q in query:
                    if rec['issn'] not in q['issn_list']:
                        data['issn_list'] = q['issn_list']
                        data['issn_list'].append(rec['issn'])

                    if edition not in q['citation_database']:
                        data['citation_database'] = q['citation_database']
                        data['citation_database'].append(edition)

                    if str(year) not in q:

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

                    if data:
                        q.modify(**data)
                        q.save()

    num_posts = models.Wos.objects().count()
    msg = u'Registred %d posts in WOS collection' % num_posts
    logger.info(msg)
    print(msg)
