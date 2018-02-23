# coding: utf-8

import csv
import logging

import models

logging.basicConfig(filename='logs/jcr_export.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)

initial_year = 1997

current_year = 2016


def formatindicator(indicator):

    data = indicator

    if indicator == 0:
        data = '0'

    if type(indicator) == str:
        if indicator == 'Not Available':
            data = None
        else:
            data = indicator

    if type(indicator) == float:
        data = indicator

    return data

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
with open('output/scielo_jcr_indicators.csv', 'w', encoding='utf-8') as csv_utf:

    spamwriter_utf = csv.writer(csv_utf, delimiter='\t')

    # Write the reader
    spamwriter_utf.writerow(header)

    # SciELO
    scielodocs = models.Scielo.objects.filter(is_jcr=1)

    for doc in scielodocs:

        jcrdocs = models.Jcr.objects(scielo_id=str(doc.id))

        for docjcr in jcrdocs:

            for year in range(initial_year, current_year + 1):

                if hasattr(docjcr, str(year)):

                    total_cites = formatindicator(docjcr[str(year)]['total_cites'])

                    journal_impact_factor = formatindicator(docjcr[str(year)]['journal_impact_factor'])

                    impact_factor_without_journal_self_cites = formatindicator(docjcr[str(year)]['impact_factor_without_journal_self_cites'])

                    five_year_impact_factor = formatindicator(docjcr[str(year)]['five_year_impact_factor'])

                    immediacy_index = formatindicator(docjcr[str(year)]['immediacy_index'])

                    citable_items = formatindicator(docjcr[str(year)]['citable_items'])

                    cited_half_life = formatindicator(docjcr[str(year)]['cited_half_life'])

                    citing_half_life = formatindicator(docjcr[str(year)]['citing_half_life'])

                    eigenfactor_score = formatindicator(docjcr[str(year)]['eigenfactor_score'])

                    article_influence_score = formatindicator(docjcr[str(year)]['article_influence_score'])

                    percentage_articles_in_citable_items = formatindicator(docjcr[str(year)]['percentage_articles_in_citable_items'])

                    average_journal_impact_factor_percentile = formatindicator(docjcr[str(year)]['average_journal_impact_factor_percentile'])

                    normalized_eigenfactor = formatindicator(docjcr[str(year)]['normalized_eigenfactor'])

                    # CSV content
                    content = [
                        doc.issn_scielo or u'',
                        str(year) or u'',
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

                    msg = '%s|%s' % (str(year), doc.issn_list)
                    logger.info(msg)
                    print(msg)

                    spamwriter_utf.writerow([l for l in content])
