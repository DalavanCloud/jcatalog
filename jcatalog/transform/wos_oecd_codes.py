# coding: utf-8
'''
This script adjusts the OECD areas in the WoS collection.
'''
import models

wos = models.Wos.objects.filter(is_scopus=0, is_scielo=0)

for doc in wos:
    if hasattr(doc, 'thematic_areas'):
        data = {}
        data['oecd'] = []
        for area in doc['thematic_areas']:  # [area1, area2]
            oecd = models.Oecd.objects.filter(wos_description=area).first()
            if oecd:
                for d in oecd['oecd']:
                    if d not in data['oecd']:
                        data['oecd'].append(d)
        print(data)
        if len(data['oecd']) > 0:
            doc.modify(**data)
            doc.save()
