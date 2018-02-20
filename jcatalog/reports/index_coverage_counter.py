# coding: utf-8
'''
Returns a list of indexes names and their occurrence number.
'''

import models

f = open('output/index_coverage_list.txt_upper', 'w')

query = models.Scielo.objects

indexes_list = []

for d in query:
    if 'api' in d:
        if 'index_coverage' in d.api:
            for i in d.api['index_coverage']:
                for element in i.split(','):
                    indexes_list.append(element.strip().upper())

indexes_list_set = set(indexes_list)

for item in indexes_list_set:
    print(item, indexes_list.count(item))
    line = '%s|%i ' % (item, indexes_list.count(item))
    f.write(line+'\n')

f.close()
