# coding: utf-8
'''
This script filters from other sources journals not present in the SciELO
collection .
'''
import models

models.Noscielo.drop_collection()

# 1) Scopus - first load in Noscielo collection
scopus = models.Scopus.objects.filter(
    publishers_country='Brazil',
    is_scielo=0,
    source_type='Journal')

print('Scopus not SciELO: %s' % scopus.count())

if scopus:
    for doc in scopus:

        noscielo = {}

        noscielo['issn_list'] = doc.issn_list
        noscielo['title'] = doc.title
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

# 2) Scimago - load of Scimago in Noscielo collection
scimago = models.Scimago.objects.filter(
    country='Brazil',
    is_scielo=0,
    is_scopus=0,
    type='journal')

print('Scimago not SciELO: %s' % scimago.count())

if scimago:
    for doc in scimago:
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

# 3) WoS - load of WoS in Noscielo collection
wos = models.Wos.objects.filter(
    country='Brazil',
    is_scielo=0,
    is_scopus=0,
    is_scimago=1)

print('WoS not SciELO: %s' % wos.count())

if wos:
    for doc in wos:
        noscielo = {}

        noscielo['issn_list'] = doc.issn_list
        noscielo['title'] = doc.title
        noscielo['wos_id'] = str(doc.id)
        noscielo['is_wos'] = doc.is_wos

        mdata = models.Noscielo(**noscielo)
        mdata.save()

# 4) Complete with 0 documents that do not have the attribute 'is_'
for doc in models.Noscielo.objects():

    if not hasattr(doc, 'is_scimago'):
        doc.modify(is_scimago=0)
        doc.save()

    if not hasattr(doc, 'is_wos'):
        doc.modify(is_wos=0)
        doc.save()

# 5) Check if is DOAJ
    for issn in doc.issn_list:
        doaj = models.Doajapi.objects.filter(issn_list=issn)
        if doaj:
            print(doaj.issn_list)
            doc.modify(
                is_doaj=1,
                doaj_id=str(doaj[0].id))
            doc.save()  # save in Noscielo Collection

            break
