# coding: utf-8

import csv
import models
import sys
import os
import logging

import alba

PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(
    filename='logs/jcr_export_indicators.info.txt',
    level=logging.INFO)
logger = logging.getLogger(__name__)


# CSV header
header = [
    'issn_scielo',
    'year',
    'total_cites',
    'journal_impact_factor',
    'impact_factor_without_journal_self_cites',
    'five_year_impact_factor',
    'immediacy_index',
    'citable_items',
    'cited_half_life',
    'citing_half_life',
    'eigenfactor_score',
    'article_influence_score',
    'percentage_articles_in_citable_items',
    'average_journal_impact_factor_percentile',
    'normalized_eigenfactor']

# Creatge the CSV file
with open('scielo_jcr_indicators.csv', 'w', encoding='utf-8') as csv_utf:
    spamwriter_utf = csv.writer(csv_utf, delimiter='\t')

    # Write the reader
    spamwriter_utf.writerow(header)

    # SciELO
    scielodocs = models.Scielo.objects

    for doc in scielodocs:

        if doc.is_wos == 1:

            docwos = models.Wos.objects(id=str(doc.wos_id))[0]

            if hasattr(docwos, 'total_cites'):
                total_cites = docwos.total_cites

            if hasattr(docwos, 'journal_impact_factor'):
                journal_impact_factor = docwos.journal_impact_factor

            if hasattr(docwos, 'impact_factor_without_journal_self_cites'):
                impact_factor_without_journal_self_cites = docwos.impact_factor_without_journal_self_cites

            if hasattr(docwos, 'five_year_impact_factor'):
                five_year_impact_factor = docwos.five_year_impact_factor

            if hasattr(docwos, 'immediacy_index'):
                immediacy_index = docwos.immediacy_index
            else:
                immediacy_index = '0'

            if hasattr(docwos, 'citable_items'):
                citable_items = docwos.citable_items

            if hasattr(docwos, 'cited_half_life'):
                cited_half_life = docwos.cited_half_life

            if hasattr(docwos, 'citing_half_life'):
                citing_half_life = docwos.citing_half_life

            if hasattr(docwos, 'eigenfactor_score'):
                 eigenfactor_score = docwos.eigenfactor_score

            if hasattr(docwos, 'article_influence_score'):
                article_influence_score = docwos.article_influence_score

            if hasattr(docwos, 'percentage_articles_in_citable_items'):
                percentage_articles_in_citable_items = docwos.percentage_articles_in_citable_items

            if hasattr(docwos, 'average_journal_impact_factor_percentile'):
                average_journal_impact_factor_percentile = docwos.average_journal_impact_factor_percentile

            if hasattr(docwos, 'normalized_eigenfactor'):
                normalized_eigenfactor = docwos.normalized_eigenfactor

            # CSV content
            content = [
                doc.issn_scielo or u'',
                u'2016',
                total_cites or u'',
                journal_impact_factor or u'',
                impact_factor_without_journal_self_cites or u'',
                five_year_impact_factor or u'',
                immediacy_index or u'',
                citable_items or u'',
                cited_half_life or u'',
                citing_half_life or u'',
                eigenfactor_score or u'',
                article_influence_score or u'',
                percentage_articles_in_citable_items or u'',
                average_journal_impact_factor_percentile or u'',
                normalized_eigenfactor or u''
            ]

            msg = doc.issn_scielo
            logger.info(msg)
            print(msg)

            spamwriter_utf.writerow([l for l in content])
