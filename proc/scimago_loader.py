# coding: utf-8
'''
This script reads data from Scimago xlsx files to process and laod in MongoDB.
'''
import os 
import sys
import models
import pyexcel
import keycorrection
import logging
from accent_remover import *
import datetime

PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename='logs/scimago_loader.info.txt',level=logging.INFO)
logger = logging.getLogger(__name__)

filelist = [f for f in os.listdir('data/scimago/xlsx')]
filelist.sort()

models.Scimago.drop_collection()

for f in filelist:

    year = f[-9:-5]
    region = f[8:-10]

    print('ini: ' + str(datetime.datetime.now()))
    print('%s %s %s' % (year, region, f))

    scimago_sheet = pyexcel.get_sheet(file_name='data/scimago/xlsx/'+f, name_columns_by_row=0)
   
    #Key correction
    for i, k in enumerate(keycorrection.scimagoall_columns_names):
        scimago_sheet.colnames[i] = k
    
    scimago_json = scimago_sheet.to_records()

    for rec in scimago_json:

        rec['title_country'] = '%s-%s' % (accent_remover(rec['title']).lower(), rec['country'].lower())
        
        issns = rec['issn'].replace('ISSN ','').replace(' ', '').split(',')
        rec['issn_list'] = [i[0:4] + '-' + i[4:8] for i in issns]

        rec = { k : v for k,v in rec.items() if v} #remove empty keys
        
        #verifica antes se existe no BD cria ou atualiza
        flag = 0

        for issn in rec['issn_list']:

            query = models.Scimago.objects.filter(issn_list = issn)
                      
            if len(query) == 0 and flag == 0:

                for k in ['sjr', 
                    'sjr_best_quartile', 
                    'h_index', 
                    'total_docs', 
                    'total_docs_3years', 
                    'total_refs', 
                    'total_cites_3years', 
                    'citable_docs_3years', 
                    'cites_by_doc_2years', 
                    'ref_by_doc']:

                    if k in rec:
                        rec['%s_%s' % (k, str(year))] = rec[k]
                        del rec[k]
                    else:
                        rec['%s_%s' % (k, str(year))] = 0

                mdata = models.Scimagoall(**rec)
                mdata.save()
                flag = 1
                break

            if len(query) == 1 and flag == 0:

                data = {}

                for k in ['sjr', 
                    'sjr_best_quartile', 
                    'h_index', 
                    'total_docs', 
                    'total_docs_3years',
                    'total_refs', 
                    'total_cites_3years', 
                    'citable_docs_3years', 
                    'cites_by_doc_2years', 
                    'ref_by_doc']:

                    if k in rec:
                        data[k + '_' + str(year)] = rec[k]
                    else:
                        data[k + '_' + str(year)] = 0

                query[0].modify(**data)
                query[0].save()
                flag = 1
                break

    num_posts = models.Scimago.objects().count()
    msg = u'Registred %d posts in Scimago collection' % num_posts
    logger.info(msg)
    print(msg)
    
    print('fim:'+str(datetime.datetime.now())+'\n')