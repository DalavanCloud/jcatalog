# coding: utf-8
'''
This script add the region Scimago in the SciELO collection.
'''
import models
from transform import collections_scielo

scielo = models.Scielo.objects

for rec in scielo:

    if 'region' not in rec and 'country' in rec:
        data = {}
        data['region'] = collections_scielo.region[rec['country']]
        print(data['region'])

    rec.modify(**data)
    rec.save()
