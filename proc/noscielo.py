# coding: utf-8

import models


models.Noscielo.drop_collection()


# 1) Scopus - first load in Noscielo
print('Scopus Not SciELO: %s' % models.Scopus.objects.filter(publishers_country='Brazil', is_scielo=0, source_type='Journal').count()) #185


for doc in models.Scopus.objects.filter(publishers_country='Brazil', is_scielo=0, source_type='Journal'):

    noscielo = {}

    noscielo['issn_list'] = doc.issn_list
    noscielo['title'] = doc.source_title
    noscielo['scopus_id'] = str(doc.id)
    noscielo['is_scopus'] = doc.is_scopus
    
    if hasattr(doc, 'scimago_id'):
        noscielo['scimago_id'] = str(doc.scimago_id)
        noscielo['is_scimago'] = doc.is_scimago
    
    if hasattr(doc, 'wos_id'):
        noscielo['wos_id'] = doc.wos_id
        noscielo['is_wos'] = doc.is_wos
    
    mdata = models.Noscielo(**noscielo)
    mdata.save()


# 2) Scimago - load of Scimago in Noscielo
print('Scimago Not SciELO: %s' % models.Scimago.objects.filter(country='Brazil', is_scielo=0).count()) #141

docs = models.Scimago.objects.filter(country='Brazil', is_scielo=0)

for doc in docs:

    if hasattr(doc, 'is_scopus'): # Scimago journals present in Scopus
        pass
    else:
        noscielo = {}

        noscielo['issn_list'] = doc.issn_list
        noscielo['title'] = doc.title
        noscielo['scimago_id'] = str(doc.id)
        noscielo['is_scimago'] = doc.is_scimago
        
        if hasattr(doc, 'wos_id'):
            noscielo['wos_id'] = doc.wos_id
            noscielo['is_wos'] = doc.is_wos
        
        mdata = models.Noscielo(**noscielo)
        mdata.save()


# 3) WoS - load of WoS in Noscielo
print('Wos Not SciELO: %s' % models.Wos.objects.filter(is_scielo=0).count()) #22

docs = models.Wos.objects.filter(country='Brazil', is_scielo=0)

for doc in docs:

    if hasattr(doc, 'is_scopus') or hasattr(doc, 'is_scimago'): # WoS journals present in Scopus or Scimago
        pass
    else:
        noscielo = {}

        noscielo['issn_list'] = doc.issn_list
        noscielo['title'] = doc.title
        noscielo['wos_id'] = str(doc.id)
        noscielo['is_wos'] = doc.is_wos
        
        mdata = models.Noscielo(**noscielo)
        mdata.save()


# 4) Complete whith 0 documents that do not have the attribute 'is_wos'
for doc in models.Noscielo.objects():
    
    if not hasattr(doc, 'is_scimago'):
        doc.modify(is_scimago=0)
        doc.save()

    if not hasattr(doc, 'is_wos'):
        doc.modify(is_wos=0)
        doc.save()
        