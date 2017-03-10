# coding: utf-8
'''
This script perform data matching from SciELO journals with other sources.
'''
import models
import logging


logging.basicConfig(filename='logs/matchlogs.txt',level=logging.INFO)
logger = logging.getLogger(__name__)


def match_jcr(issn_scielo, coldb):
    for doc in coldb:
        for issn in doc.issn_list:
            if issn_scielo == issn:
                result = (1, issn)
                return result

def main():
    for doc in models.Scielo.objects:
        for issn_scielo in doc.issn_list:
            #JCR
            coldb = models.Jcr.objects
            jcr = match_jcr(issn_scielo, coldb)
            if jcr is not None and jcr[0] == 1:
                 print('ISSN SciELO %s is JCR: %s' % (issn_scielo, jcr[1]))

            #Scimago
            coldb = models.Scimago.objects
            scimago = match_jcr(issn_scielo, coldb)
            if jcr is not None and jcr[0] == 1:
                 print('ISSN SciELO %s is Scimago: %s' % (issn_scielo, scimago[1]))


if __name__ == "__main__":
    main()
