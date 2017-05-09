# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import os 
import sys
import models
import pyexcel
import keycorrection
import collections_scielo
import logging
from transform import *

PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename='logs/procstore.info.txt',level=logging.INFO)
logger = logging.getLogger(__name__)


def scieloproc():
    scielo_sheet  = pyexcel.get_sheet(file_name='data/scielo/journals_scl.csv', name_columns_by_row=0)
    
    #Key correction
    for i, k in enumerate(keycorrection.scielo_columns_names):
        scielo_sheet.colnames[i] = k
    
    scielo_json = scielo_sheet.to_records()

    models.Scielo.drop_collection()

    for rec in scielo_json:

        rec['country'] = collections_scielo.country[rec['collection']]

        rec['title_at_scielo_country'] = '%s-%s' % (rec['title_at_scielo'], rec['country'])

        #convert issn int type to str type
        if type(rec['issns']) != str: 
            rec['issns'] = Issn().issn_hifen(rec['issns'])
            msg = u'issn modificado: %s - %s' % (rec['issns'],rec['title_at_scielo'])
            logger.info(msg)
        
        #convert in list
        if type(rec['issns']) == str: 
            rec['issns'] = rec['issns'].split(';') 
            rec['issn_list'] = []
            rec['issn_list'].append(rec['issn_scielo'])
            for i in rec['issns']:
                if i not in rec['issn_scielo']:
                    rec['issn_list'].append(i)

        #transform data in datetime type
        rec['date_of_the_first_document'] = Dates().data2datetime(rec['date_of_the_first_document'])
        rec['date_of_the_last_document'] = Dates().data2datetime(rec['date_of_the_last_document'])

        rec = { k : v for k,v in rec.items() if v} #remove empty keys

        mdata = models.Scielo(**rec)
        mdata.save()

    num_posts = models.Scielo.objects().count()
    msg = u'Registred %d posts in SciELO collection' % num_posts
    logger.info(msg)
    print(msg)


def scimagoproc():
    scimago_sheet = pyexcel.get_sheet(file_name='data/scimago/scimago_all_r5_conso.xlsx', name_columns_by_row=0)
    
    #Key correction
    for i, k in enumerate(keycorrection.scimago_columns_names):
        scimago_sheet.colnames[i] = k
    
    scimago_json = scimago_sheet.to_records()
    
    models.Scimago.drop_collection()
    
    for rec in scimago_json:

        rec['title_country'] = '%s-%s' % (rec['title'],rec['country'])
        
        #issns = rec['issn'].replace('ISSN ','').replace(' ', '').split(',')
        #rec['issn_list'] = [i[0:4] + '-' + i[4:8] for i in issns]
        rec['issn_list'] = []
        if rec['issn1']:
            rec['issn_list'].append(rec['issn1'])
        if rec['issn2']:
            rec['issn_list'].append(rec['issn2'])
        if rec['issn3']:
            rec['issn_list'].append(rec['issn3'])

        rec = { k : v for k,v in rec.items() if v} #remove empty keys
        
        mdata = models.Scimago(**rec)
        mdata.save()

    num_posts = models.Scimago.objects().count()
    msg = u'Registred %d posts in Scimago collection' % num_posts
    logger.info(msg)
    print(msg)


def scopusproc():
    scopus_sheet = pyexcel.get_sheet(file_name='data/scopus/title_list.xlsx', name_columns_by_row=0)

    #Key correction
    for i, k in enumerate(keycorrection.scopus_columns_names):
        scopus_sheet.colnames[i] = k
    
    scopus_sheet.column.format('print_issn', str)
    scopus_sheet.column.format('e_issn', str)
    scopus_json = scopus_sheet.to_records()

    models.Scopus.drop_collection()

    for i, rec in enumerate(scopus_json): #ISSN normalization
        #print('\nrec:' + str(i))
        
        rec['issn_list']=[]
        if rec['print_issn']:
            rec['issn_list'].append(rec['print_issn'][0:4] + '-' + rec['print_issn'][4:8])
        if rec['e_issn']:
            rec['issn_list'].append(rec['e_issn'][0:4] + '-' + rec['e_issn'][4:8])

        rec = { k : v for k,v in rec.items() if v} #remove empty keys

        mdata = models.Scopus(**rec)
        mdata.save()

    num_posts = models.Scopus.objects().count()
    msg = u'Registred %d posts in Scopus collection' % num_posts
    logger.info(msg)
    print(msg)


def wosproc():
    jcr_sheet  = pyexcel.get_sheet(file_name='data/jcr/JournalHomeGrid.csv', name_columns_by_row=0)
    
    #Key correction
    for i, k in enumerate(keycorrection.jcr_columns_names):
        jcr_sheet.colnames[i] = k
    
    jcr_json_dup = jcr_sheet.to_records()
    
    jcr_json = []

    for rec in jcr_json_dup: #remove duplicates
        if rec not in jcr_json:
            jcr_json.append(rec)

    models.Wos.drop_collection()

    for rec in jcr_json:
        
        rec['issn_list']=[rec['issn']]

        rec = { k : v for k,v in rec.items() if v} #remove empty keys

        mdata = models.Wos(**rec)
        mdata.save()

    num_posts = models.Wos.objects().count()
    msg = u'Registred %d posts in WOS collection' % num_posts
    logger.info(msg)
    print(msg)


def cwtsproc():
    cwts_sheet = pyexcel.get_sheet(file_name='data/cwts/CWTS_Journal_Indicators_June_2016_r5c_extrato.xlsx', name_columns_by_row=0)
    
    #Key correction
    for i, k in enumerate(keycorrection.cwts_columns_names):
        cwts_sheet.colnames[i] = k
    
    cwts_json = cwts_sheet.to_records()

    models.Cwts.drop_collection()
    
    for rec in cwts_json:

        rec['issn_list']=[]
        if rec['print_issn'] and len(rec['print_issn']) > 2:
            rec['issn_list'].append(rec['print_issn'])
        if rec['electronic_issn'] and len(rec['electronic_issn']) > 2:
            rec['issn_list'].append(rec['electronic_issn'])

        rec = { k : v for k,v in rec.items() if v} #remove empty keys
        
        mdata = models.Cwts(**rec)
        mdata.save()

    num_posts = models.Cwts.objects().count()
    msg = u'Registred %d posts in CWTS collection' % num_posts
    logger.info(msg)
    print(msg)


def doajproc():
    doaj_sheet = pyexcel.get_sheet(file_name='data/doaj/controle_DOAJ.xlsx', name_columns_by_row=0)
    
    #Key correction
    for i, k in enumerate(keycorrection.doaj_columns_names):
        doaj_sheet.colnames[i] = k
    
    doaj_json = doaj_sheet.to_records()

    models.Doaj.drop_collection()
    
    for rec in doaj_json:

        rec['issn_list']=[]
        rec['issn_list'].append(rec['issn'])
        
        rec = { k : v for k,v in rec.items() if v} #remove empty keys
        
        mdata = models.Doaj(**rec)
        mdata.save()

    num_posts = models.Doaj.objects().count()
    msg = u'Registred %d posts in DOAJ collection' % num_posts
    logger.info(msg)
    print(msg)


def submissions():# Add OJS and ScholarOne
    submiss_sheet = pyexcel.get_sheet(file_name='data/submiss/sistemas_submissao_scielo_brasil.xlsx', name_columns_by_row=0)

    #Key correction
    for i, k in enumerate(keycorrection.submission_scielo_brasil_columns_names):
        submiss_sheet.colnames[i] = k

    submiss_json = submiss_sheet.to_records()

    models.Submissions.drop_collection()

    for rec in submiss_json:

        rec['issn_list']=[]
        rec['issn_list'].append(rec['issn_scielo'])
        
        rec = { k : v for k,v in rec.items() if v} #remove empty keys
        
        mdata = models.Submissions(**rec)
        mdata.save()

    num_posts = models.Submissions.objects().count()
    msg = u'Registred %d posts in Submissions collection' % num_posts
    logger.info(msg)
    print(msg)


def main():
    # SciELO - csv
    scieloproc()

    # Scimago - xlsx
    scimagoproc()

    # Scopus - xlsx
    scopusproc()

    # WOS - csv
    wosproc()

    # CWTS - xlsx
    cwtsproc()

    # DOAJ - xlsx
    doajproc()

    # Submissions - xlsx
    submissions()


if __name__ == "__main__":
    main()
