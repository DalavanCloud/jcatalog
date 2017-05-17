# coding: utf-8

import models


models.Noscielo.drop_collection()

print('Scopus Not SciELO: %s' % models.Scopus.objects.filter(publishers_country='Brazil', is_scielo=0, source_type='Journal').count()) #185
for doc in models.Scopus.objects.filter(publishers_country='Brazil', is_scielo=0, source_type='Journal'):
    noscielo = {}
    noscielo['issn_list'] = doc.issn_list
    noscielo['title'] = doc.source_title
    noscielo['scopus_id'] = str(doc.id)
    noscielo['is_scopus'] = doc.is_scopus
    mdata = models.Noscielo(**noscielo)
    mdata.save()

print('Scimago Not SciELO: %s' % models.Scimago.objects.filter(country='Brazil', is_scielo=0).count()) #140
for doci in models.Noscielo.objects():
    for issn in doci.issn_list:
        result = models.Scimago.objects.filter(country='Brazil', is_scielo=0, issn_list=issn)
        print(issn)
        if result:
            for r in result:
                doci.modify(
                    is_scimago = 1,
                    scimago_id = str(r.id))
                doci.save()
                pass


    tresult = models.Scimago.objects.filter(country='Brazil', is_scielo=0, title__iexact=doci.title)
    if tresult:
        for t in tresult:
            doci.modify(
                is_scimago = 1, 
                scimago_id = str(t.id))
            doci.save()
            pass

for doci in models.Noscielo.objects():
    if not hasattr(doci, 'is_scimago'):
        doci.modify(is_scimago=0)
        doci.save()


print('----------------------------------------')
print('Wos Not SciELO: %s' % models.Wos.objects.filter(is_scielo=0).count()) #22
for docw in models.Noscielo.objects():
    for issn in docw.issn_list:
        resultw = models.Wos.objects.filter(is_scielo=0, issn_list=issn)
        print(issn)
        if resultw:
            for r in resultw:
                docw.modify(
                    is_wos = 1,
                    wos_id = str(r.id) 
                    )
                docw.save()
                pass

    tresult = models.Wos.objects.filter(is_scielo=0, full_journal_title__iexact=docw.title)
    if tresult:
        for tr in tresult:
            print('wos:'+tr.full_journal_title)
            print('isw:'+str(tr.is_wos))
            docw.modify(
                is_wos = 1, 
                wos_id = str(tr.id))
            docw.save()
            pass
    
    print(models.Noscielo.objects.get(id=str(docw.id)).to_json())
    print('\n')


for docw in models.Noscielo.objects():
    if not hasattr(docw, 'is_wos'):
        docw.modify(is_wos=0)
        docw.save()
