# coding: utf-8
'''
This script reads data from Scopus CiteScore to process and store in MongoDB.
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

logging.basicConfig(filename='logs/procstore.info.txt',level=logging.INFO)
logger = logging.getLogger(__name__)


def scopuscs():
    scopus_sheet = pyexcel.get_sheet(file_name='data/scopus/CiteScore_Metrics_2011-2016_Download_21Jun2017.xlsx', name_columns_by_row=0)

    #Key correction
    for i, k in enumerate(keycorrection.scopuscitscore_columns_names):
        scopus_sheet.colnames[i] = k
    
    scopus_sheet.column.format('print_issn', str)
    scopus_sheet.column.format('eissn', str)
    scopus_json = scopus_sheet.to_records()

    models.Scopuscitescore.drop_collection()

    for i, rec in enumerate(scopus_json): #ISSN normalization
        
        #rec['title_country'] = '%s-%s' % (accent_remover(rec['title']).lower(), rec['publishers_country'].lower())
        
        if len(rec['eissn']) == 5:
            rec['eissn'] = '000' + str(rec['eissn'])
        if len(rec['eissn']) == 6:
            rec['eissn'] = '00' + str(rec['eissn'])
        if len(rec['eissn']) == 7:
            rec['eissn'] = '0' + str(rec['eissn'])

        if len(rec['print_issn']) == 5:
            rec['print_issn'] = '000' + str(rec['print_issn'])
        if len(rec['print_issn']) == 6:
            rec['print_issn'] = '00' + str(rec['print_issn'])
        if len(rec['print_issn']) == 7:
            rec['print_issn'] = '0' + str(rec['print_issn'])

        rec['issn_list']=[]
        if rec['print_issn']:
            rec['issn_list'].append(rec['print_issn'][0:4] + '-' + rec['print_issn'][4:8])
        if rec['eissn']:
            rec['issn_list'].append(rec['eissn'][0:4] + '-' + rec['eissn'][4:8])

        rec = { k : v for k,v in rec.items() if v} #remove empty keys

        mdata = models.Scopuscitescore(**rec)
        mdata.save()

    num_posts = models.Scopuscitescore.objects().count()
    msg = u'Registred %d posts in Scopus CiteScore collection' % num_posts
    logger.info(msg)
    print(msg)


def main():
    # Scopus CiteScore - xlsx
    scopuscs()


if __name__ == "__main__":
    main()
