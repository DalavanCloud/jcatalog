# coding: utf-8

import csv
import logging

import models

logging.basicConfig(filename='logs/scopus_export.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)

initial_year = 1999

current_year = 2016


def formatindicator(indicator):

    data = indicator

    if indicator == 0:
        data = '0'

    return data

# CSV header
header = [
    'issn_scielo',
    'year',
    'scopus_id',  # scopus
    'citescore',
    'sjr',  # scimago
    'sjr_best_quartile',
    'cites_by_doc_2years',
    'h_index',
    'snip',  # cwts
    'ipp']

# Creatge the CSV file
with open('output/scielo_scopus_indicators.csv', 'w', encoding='utf-8') as csv_utf:

    spamwriter_utf = csv.writer(csv_utf, delimiter='\t')

    # Write the reader
    spamwriter_utf.writerow(header)

    # SciELO
    scielodocs = models.Scielo.objects

    for docscielo in scielodocs:
        print(docscielo.title)

        hasscimago = 0
        hasscopus = 0
        hascwts = 0

        for year in range(initial_year, current_year + 1):

            if 'scimago_id' in docscielo:

                scimago = models.Scimago.objects(id=str(docscielo.scimago_id))

                for doc in scimago:

                    if hasattr(doc, str(year)):
                        sjr = doc[str(year)]['sjr']
                        sjr_best_quartile = doc[str(year)]['sjr_best_quartile']
                        cites_by_doc_2years = formatindicator(doc[str(year)]['cites_by_doc_2years'])
                        h_index = doc[str(year)]['h_index']
                        hasscimago = 1
                    else:
                        sjr = None
                        sjr_best_quartile = None
                        cites_by_doc_2years = None
                        h_index = None
                        hasscimago = 0

            if 'cwts_id' in docscielo:

                cwts = models.Cwts.objects(id=str(docscielo.cwts_id))

                for doc in cwts:

                    if hasattr(doc, str(year)):
                        snip = formatindicator(doc[str(year)]['snip'])
                        ipp = formatindicator(doc[str(year)]['ipp'])
                        hascwts = 1
                    else:
                        snip = None
                        ipp = None
                        hascwts = 0

            if 'scopus_id' in docscielo:

                scopus = models.Scopus.objects(id=str(docscielo.scopus_id))

                for doc in scopus:

                    if hasattr(doc, str(year)):
                        if 'citescore' in doc[str(year)]:
                            citescore = formatindicator(doc[str(year)]['citescore'])
                            hasscopus = 1
                    else:
                        citescore = None
                        scopus_id = None
                        hasscopus = 0

            if hasscimago == 1 or hascwts == 1 or hasscopus == 1:
                if 'scopus_id' in docscielo:
                    scopus = models.Scopus.objects(id=str(docscielo.scopus_id))
                    scopus_id = scopus[0]['sourcerecord_id']

            # CSV content
            if hasscimago == 1 or hascwts == 1 or hasscopus == 1:

                content = [
                    docscielo.issn_scielo or u'',
                    year or u'',
                    scopus_id or u'',
                    citescore or u'',
                    sjr or u'',
                    sjr_best_quartile or u'',
                    cites_by_doc_2years or u'',
                    h_index or u'',
                    snip or u'',
                    ipp or u''
                ]

                msg = '%s|%s' % (str(year), docscielo.issn_scielo)
                logger.info(msg)
                print(msg)

                spamwriter_utf.writerow([l for l in content])
