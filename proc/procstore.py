# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''

import models
import pyexcel


def scieloproc():
    scielosheet = pyexcel.get_sheet(file_name='data/scielo/journals.csv', name_columns_by_row=0)
    scielosheet.column.format('extraction date', str)
    scielojson = scielosheet.to_records()
    
    models.Scielo.drop_collection()

    for rec in scielojson:
        for key in rec.keys(): #key adjustments - in test
            rec[key.lower().replace(' ','_').replace("'","")] = rec.pop(key)

        rec = { k : v for k,v in rec.items() if v} #remove empty keys

        mdata = models.Scielo(**rec)
        mdata.save()

    num_posts = models.Scielo.objects().count()
    print('Registred %d posts in SciELO collection' % num_posts)


def scimagoproc():
    scimagosheet = pyexcel.get_sheet(file_name='data/scimago/scimago_Latin America_2015.xlsx', name_columns_by_row=0)
    scimagojson = scimagosheet.to_records()
    
    models.Scimago.drop_collection()
    
    for rec in scimagojson: #key adjustments - in test
        for key in rec.keys():
            rec[key.lower().replace(' ','_').replace("'","")] = rec.pop(key)
 
        issns = rec['issn'].split(',') #ISSN normalization

        for e,i in enumerate(issns):
            try:
                if e == 0:
                    rec['issn'+str(e+1)] = i[5:9]+'-'+i[9:13]
                else:
                    rec['issn'+str(e+1)] = i[1:5]+'-'+i[5:10]
            except IndexError:
                None

        rec = { k : v for k,v in rec.items() if v} #remove empty keys
        
        mdata = models.Scimago(**rec)
        mdata.save()

    num_posts = models.Scimago.objects().count()
    print('Registred %d posts in Scimago collection' % num_posts)


def scopusproc():
    scopussheet = pyexcel.get_sheet(file_name='data/scopus/title_list_keys_ok.xlsx', name_columns_by_row=0)
    scopussheet.column.format('Print-ISSN', str)
    scopussheet.column.format('E-ISSN', str)
    scopusjson = scopussheet.to_records()

    models.Scopus.drop_collection()

    for rec in scopusjson: #key adjustments - in test
        for key in rec.keys():
            rec[key.lower().replace('\n\n','_').replace('\n','_').replace(':','').replace(' ','_').replace("'","")] = rec.pop(key)

    for i, rec in enumerate(scopusjson): #ISSN normalization
        print('\nrec:' + str(i))
        try:
            if rec['print-issn']:
                rec['issn1'] = rec['print-issn'][0:4] + '-' + rec['print-issn'][4:8]
        except IndexError:
            None
        try:
            if rec['e-issn']:
                rec['issn2'] = rec['e-issn'][0:4] + '-' + rec['e-issn'][4:8]
        except IndexError:
            None

        rec = { k : v for k,v in rec.items() if v} #remove empty keys

        mdata = models.Scopus(**rec)
        mdata.save()

    num_posts = models.Scopus.objects().count()
    print('Registred %d posts in Scopus collection' % num_posts)


def main():
    #SciELO - csv
    scieloproc()

    #Scimago - xlsx
    scimagoproc()

    #Scopus - xlsx
    scopusproc()


if __name__ == "__main__":
    main()