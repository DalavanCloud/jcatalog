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

logging.basicConfig(filename='logs/scopus_update.txt',level=logging.INFO)
logger = logging.getLogger(__name__)


def scopuscs(year):
    scopus_sheet = pyexcel.get_sheet(file_name='data/scopus/CiteScore_Metrics_2011-2016_Download_21Jun2017_import.xlsx', 
        sheet_name='2011 All', 
        name_columns_by_row=0)

    #Key correction
    for i, k in enumerate(keycorrection.scopuscitscore_columns_names):
        scopus_sheet.colnames[i] = k
    
    scopus_sheet.column.format('print_issn', str)
    scopus_sheet.column.format('eissn', str)
    scopus_json = scopus_sheet.to_records()

    for rec in scopus_json:
        
        rec = { k : v for k,v in rec.items() if v} #remove empty keys
        
        print('%s %s' % (type(rec['scopus_sourceid']), rec['scopus_sourceid']))
        
        query = models.Scopus.objects.filter(sourcerecord_id = rec['scopus_sourceid'])

        if len(query) == 1:

            data = {}
            
            for k in ['citescore', 'sjr', 'snip']:

                if not year in data and k in rec: 
                    data = {year:{}}
                if k in rec and rec[k] != '':
                    data[year].update({k:float(rec[k])})

            if len(data) > 0:
                query[0].modify(**data)
                query[0].save()  # save in Scopus

def main():
    scopuscs('2011')


if __name__ == "__main__":
    main()
