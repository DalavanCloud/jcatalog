# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''

import models
import pyexcel
import keycorrection   
import logging


logging.basicConfig(filename='logs/logs.txt',level=logging.INFO)

logger = logging.getLogger(__name__)

def scieloproc():
    scielo_sheet  = pyexcel.get_sheet(file_name='data/scielo/journals.csv', name_columns_by_row=0)
     
    scielo_sheet.column.format('extraction date', str)
    
    #Key correction
    for i, k in enumerate(keycorrection.scielo_columns_names):
        scielo_sheet.colnames[i] = k
    
    scielo_json = scielo_sheet.to_records()

    models.Scielo.drop_collection()

    for rec in scielo_json:

        rec['is_scielo'] = 1 #counter
        
        rec['issns'] = rec['issns'].split(';') #convert in list
        
        rec = { k : v for k,v in rec.items() if v} #remove empty keys

        mdata = models.Scielo(**rec)

        mdata.save()

    num_posts = models.Scielo.objects().count()
    msg = u'Registred %d posts in SciELO collection' % num_posts
    logger.info(msg)


def scimagoproc():
    scimago_sheet = pyexcel.get_sheet(file_name='data/scimago/scimago_Latin America_2015.xlsx', name_columns_by_row=0)
    
    #Key correction
    for i, k in enumerate(keycorrection.scimago_columns_names):
        scimago_sheet.colnames[i] = k
    
    scimago_json = scimago_sheet.to_records()
    
    models.Scimago.drop_collection()
    
    for rec in scimago_json:

        rec['is_scimago'] = 1 #counter
        
        issn_list = rec['issn'].replace('ISSN ','').replace(' ', '').split(',')

        rec['issn_list'] = [i[0:4] + '-' + i[4:8] for i in issn_list]

        rec = { k : v for k,v in rec.items() if v} #remove empty keys
        
        mdata = models.Scimago(**rec)

        mdata.save()

    num_posts = models.Scimago.objects().count()
    print('Registred %d posts in Scimago collection' % num_posts)


def scopusproc():
    scopus_sheet = pyexcel.get_sheet(file_name='data/scopus/title_list_keys_ok.xlsx', name_columns_by_row=0)
    scopus_sheet.column.format('Print-ISSN', str)
    scopus_sheet.column.format('E-ISSN', str)
    scopus_json = scopus_sheet.to_records()

    models.Scopus.drop_collection()

    for rec in scopus_json:

        rec['is_scopus'] = 1 #counter

        for key in rec.keys(): #key adjustments - in test
            rec[key.lower().replace('\n\n','_').replace('\n','_').replace(':','').replace(' ','_').replace("'","")] = rec.pop(key)

    for i, rec in enumerate(scopus_json): #ISSN normalization
        
        print('\nrec:' + str(i))
        
        try:
            if rec['print-issn']:
                rec['issn1'] = rec['print-issn'][0:4] + '-' + rec['print-issn'][4:8]
        except IndexError as e:
            print(e)

        try:
            if rec['e-issn']:
                rec['issn2'] = rec['e-issn'][0:4] + '-' + rec['e-issn'][4:8]
        except IndexError as e:
            print(e)

        rec = { k : v for k,v in rec.items() if v} #remove empty keys

        mdata = models.Scopus(**rec)

        mdata.save()

    num_posts = models.Scopus.objects().count()
    print('Registred %d posts in Scopus collection' % num_posts)


def jcrproc():
    jcr_sheet  = pyexcel.get_sheet(file_name='data/jcr/JournalHomeGrid.csv', name_columns_by_row=0)
    
    #Key correction
    for i, k in enumerate(keycorrection.jcr_columns_names):
        jcr_sheet.colnames[i] = k
    
    jcr_json = jcr_sheet.to_records()

    models.Jcr.drop_collection()

    for rec in jcr_json:

        rec['is_jcr'] = 1 #counter
        
        rec = { k : v for k,v in rec.items() if v} #remove empty keys

        mdata = models.Jcr(**rec)

        mdata.save()

    num_posts = models.Jcr.objects().count()
    msg = u'Registred %d posts in JCR collection' % num_posts
    logger.info(msg)


def main():
    #SciELO - csv
    scieloproc()

    #Scimago - xlsx
    scimagoproc()

    #Scopus - xlsx
    #scopusproc()

    #JCR - csv
    jcrproc()


if __name__ == "__main__":
    main()
