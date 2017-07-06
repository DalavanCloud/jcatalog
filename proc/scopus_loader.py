# coding: utf-8
'''
This script reads data from Scopus xlsx files to process and laod in MongoDB.
'''
import os 
import sys
import models
import pyexcel
import keycorrection
import logging
from transform import *
from accent_remover import *


PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename='logs/scopus_loader.info.txt',level=logging.INFO)
logger = logging.getLogger(__name__)

models.Scopus.drop_collection()

def scopusproc(file_name, keys):

    sheet = pyexcel.get_sheet(file_name=file_name, name_columns_by_row=0)
   
    #Key correction
    for i, k in enumerate(keys):
        sheet.colnames[i] = k
    
    sheet.column.format('print_issn', str)
    sheet.column.format('e_issn', str)
    sheet_json = sheet.to_records()

    for rec in sheet_json:
        print(rec['sourcerecord_id'])

        #rec['title_country'] = '%s-%s' % (accent_remover(rec['title']).lower(), rec['country'].lower())
        
        rec['issn_list'] = []

        if rec['print_issn']:
            rec['issn_list'].append(rec['print_issn'][0:4] + '-' + rec['print_issn'][4:8])

        if rec['e_issn']:
            rec['issn_list'].append(rec['e_issn'][0:4] + '-' + rec['e_issn'][4:8])

        rec = { k : v for k,v in rec.items() if v} #remove empty keys
        
        for year in ['2014', '2015', '2016']:

            for k in ['citescore', 'sjr', 'snip']:

                if k+'_'+year in rec:

                    if not year in rec:
                        rec[year]={}
                
                    rec[year].update({k:float(rec[k+'_'+year])})
                    
                    del rec[k+'_'+year]

        mdata = models.Scopus(**rec)
        mdata.save()

    num_posts = models.Scopus.objects().count()
    msg = u'Registred %d posts in Scopus test collection' % num_posts
    logger.info(msg)
    print(msg)
    

def main():
    '''
    scopusproc(file_name, keycorrection)
        file_name = xlsx path and file name
    keycorrection = dict name of keycorrection module
    ''' 
    scopusproc('data/scopus/ext_list_June_2017.xlsx', keycorrection.scopus_columns_names_2016)


if __name__ == "__main__":
    main()
