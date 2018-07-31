import csv
from articlemeta.client import RestfulClient


cl = RestfulClient()

issn_list = []

with open('issn_list_scielo_network2.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile)

    filewriter.writerow(
        [
            'unique issn',
            'issn scielo',
            'print issn',
            'electronic issn',
            'title',
            'status',
            'acronym',
            'country'
        ])

    for c in [
            #'arg',
            'bol'
            # 'chl',
            # 'col',
            # 'cri',
            # 'cub',
            # 'esp',
            # 'mex',
            # 'per',
            # 'prt',
            # 'scl',
            # 'sza',
            # 'ury',
            # 'ven'
    ]:

        for j in cl.journals(collection=c):

            status = None
            status = j.current_status

            if status == 'current':

                jil = []

                if j.scielo_issn not in jil:
                    jil.append(j.scielo_issn)
                if j.print_issn not in jil:
                    jil.append(j.print_issn)
                if j.electronic_issn not in jil:
                    jil.append(j.electronic_issn)
                if j.any_issn() not in jil:
                    jil.append(j.any_issn())

                njil = set(jil)

                for n in jil:
                    if n:
                        print(n + '|' + j.collection_acronym + '|' + j.title)
                        content = [
                            n or u'',
                            j.scielo_issn or u'',
                            j.print_issn or u'',
                            j.electronic_issn or u'',
                            j.title or u'',
                            j.current_status or u'',
                            j.collection_acronym or u'',
                            j.publisher_country[1] or u''
                        ]

                        filewriter.writerow([l for l in content])
