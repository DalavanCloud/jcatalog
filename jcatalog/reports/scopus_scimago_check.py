# coding: utf-8
import csv
import logging

import models
from accent_remover import *

logging.basicConfig(filename='logs/scimago_check2.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)

# CSV header
header = [
    'scielo_issn',
    'collection',
    'scielo_status',
    'final_year',
    'scielo_not_scimago',
    'is_scielo',  # is
    'is_scopus',
    'is_scimago',
    'scimago_filter_by_scielo',  # filter
    'scimago_region',  # region
    'scielo_issns',  # issns
    'scopus_issns',
    'scimago_issns',
    'scielo_title',  # title
    'scopus_title',
    'scimago_title',
    'diff_scopus_title',
    'diff_scimago_title',
    'scielo_publisher',  # publisher
    'scopus_publisher',
    'diff_publisher',
    'scielo_country',  # country
    'scopus_country',
    'scimago_country',
    'diff_scopus_country',
    'diff_scimago_country'
    ]

# Create the CSV file
with open('output/scopus_scimago_check2.csv', 'w', encoding='utf-8') as csv_utf:

    spamwriter_utf = csv.writer(csv_utf, delimiter='\t')

    # Write the reader
    spamwriter_utf.writerow(header)

    # SciELO
    scielodocs = models.Scielo.objects

    for scielo in scielodocs:
        print(scielo.title)
        scielo_title_low = accent_remover(scielo.title.lower().replace(' & ', ' and ').replace('&', ' and '))
        scielo_publisher_low = accent_remover(scielo.publisher_name.lower().replace(' & ', ' and ').replace('&', ' and '))
        difftitlescopus = None
        difftitlescimago = None
        diffcountryscopus = None
        diffcountryscimago = None
        diffpublisherscopus = None
        filter_scielo = None

        scielo_final_year = None
        if 'stopping_year_at_scielo' in scielo:
            scielo_final_year = scielo.stopping_year_at_scielo

        # scopus
        scopus_issns = None
        scopus_title = None
        scopus_country = None
        scopus_publisher = None
        if 'scopus_id' in scielo:

            scopus = models.Scopus.objects(id=str(scielo.scopus_id))[0]
            scopus_issns = '; '.join(scopus.issn_list)
            scopus_title = scopus.title
            scopus_country = scopus.country
            scopus_publisher = scopus.publishers_name
            # title
            difftitlescopus = None
            if scielo_title_low != accent_remover(scopus.title.lower().replace(' & ', ' and ').replace('&', ' and ')):
                difftitlescopus = 1
            else:
                difftitlescopus = 0

            # country
            diffcountryscopus = None
            if scielo.country != scopus.country:
                diffcountryscopus = 1
            else:
                diffcountryscopus = 0

            # publisher
            diffpublisherscopus = None
            if scielo_publisher_low != accent_remover(scopus.publishers_name.lower().replace(' & ', ' and ').replace('&', ' and ')):
                diffpublisherscopus = 1
            else:
                diffpublisherscopus = 0
        else:
            scopus = None

        # scimago
        scimago_issns = None
        scimago_title = None
        scimago_country = None
        scimago_region = None
        if 'scimago_id' in scielo:

            scimago = models.Scimago.objects(id=str(scielo.scimago_id))[0]
            scimago_issns = '; '.join(scimago.issn_list)
            scimago_title = scimago.title
            scimago_country = scimago.country
            scimago_region = scimago.region

            # filter by scielo
            filter_scielo = None
            if 'inscielo' in scimago:
                filter_scielo = 1
            else:
                filter_scielo = 0

            # title
            difftitlescimago = None
            if scielo_title_low != accent_remover(scimago_title.lower().replace(' & ', ' and ').replace('&', ' and ')):
                difftitlescimago = 1
            else:
                difftitlescimago = 0

            # country
            diffcountryscimago = None
            if scielo.country != scimago.country:
                diffcountryscimago = 1
            else:
                diffcountryscimago = 0
        else:
            scimago = None

        # Analise
        scielo_no_scimago = 'sem'
        if scielo.title_current_status == 'current':
            if 'scimago_id' in scielo:
                if filter_scielo == 1:
                    scielo_no_scimago = 0
            if 'scimago_id' in scielo:
                if filter_scielo == 0:
                    scielo_no_scimago = 1
            if 'scimago_id' not in scielo:
                scielo_no_scimago = 1  # nao esta no Scimago

        if scielo.title_current_status != 'current':
            scielo_no_scimago = None  # Branco

        # CSV content
        # if scopus is not None or scimago is not None:
        content = [
            scielo.issn_scielo or u'',
            scielo.collection or u'',
            scielo.title_current_status or u'',
            scielo_final_year or u'',
            scielo_no_scimago,
            scielo.is_scielo or 0,
            scielo.is_scopus or 0,
            scielo.is_scimago or 0,
            filter_scielo or 0,
            scimago_region or u'',
            '; '.join(scielo.issn_list) or u'',
            scopus_issns or u'',
            scimago_issns or u'',
            scielo.title or u'',
            scopus_title or u'',
            scimago_title or u'',
            difftitlescopus or 0,
            difftitlescimago or 0,
            scielo.publisher_name or u'',
            scopus_publisher or u'',
            diffpublisherscopus or 0,
            scielo.country or u'',
            scopus_country or u'',
            scimago_country or u'',
            diffcountryscopus or 0,
            diffcountryscimago or 0,

        ]

        msg = '%s' % (scielo.issn_scielo)
        logger.info(msg)
        print(msg)

        spamwriter_utf.writerow([l for l in content])


# Scimago
# with open('output/scimago_inscielo_noscielo.csv', 'w', encoding='utf-8') as csv_utf:

#     spamwriter_utf = csv.writer(csv_utf, delimiter='\t')

#     # Write the reader
#     spamwriter_utf.writerow(header)

#     scimagodocs = models.Scimago.objects.filter(inscielo=1, is_scielo=0)

#     for docscimago in scimagodocs:
#         print(docscimago.title)

#         filter_scielo = None
#         if 'inscielo' in docscimago:
#             filter_scielo = 1
#         else:
#             filter_scielo = 0

#         # CSV content
#         content = [
#            '; '.join(docscimago.issn_list) or u'',
#             docscimago.title or u'',
#             docscimago.country or u'',
#             docscimago.is_scopus or u'',
#             docscimago.is_scimago or u'',
#             docscimago.region or u'',
#             filter_scielo or 0,
#             ]
#         msg = '%s' % (docscimago.issn)
#         logger.info(msg)
#         print(msg)

#         spamwriter_utf.writerow([l for l in content])
