from articlemeta.client import RestfulClient

import csv

cl = RestfulClient()

issn_list = []

for c in [
        'arg',
        'bol',
        'chl',
        'col',
        'cri',
        'cub',
        'esp',
        'mex',
        'per',
        'prt',
        'scl',
        'sza',
        'ury',
        'ven']:

    for journal in cl.journals(collection=c):
        status = None
        status = journal.current_status
        if status == 'current':
            print('issn_api: ' + journal.scielo_issn)
            issn_list.append(journal.scielo_issn)
            issn_list.append(journal.print_issn)
            issn_list.append(journal.electronic_issn)
            issn_list.append(journal.any_issn())

unique_issn_list = set(issn_list)

with open('issn_list_scielo_network.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile)

    for issn in unique_issn_list:
        # print('issn_unique: ' + str(issn))
        filewriter.writerow([issn])
