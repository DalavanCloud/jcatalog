# coding: utf-8
'''
Extrai da base jcatalog a lista de ISSNs agregando a chave "account"
para consulta no Google Analytics e relatorio SciELO 20 anos.
'''

from pprint import pprint
import models

collection_issn_list = []

'''
Accounts in Google Analytics
This list was obtained by scraping the Google Analytics - Query Explorer,
combo list "Account" and added your key "collection".
'''
accounts = {
    "scl": "www.scielo.br",
    "arg": "www.scielo.org.ar/",
    # "bol" Bolivia nao está no Google Analytics
    "chl": "www.scielo.cl",
    "col": "www.scielo.org.co",
    "cri": "www.scielo.sa.cr",
    "cub": "scielocuba",
    "esp": "scielo.isciii.es",
    "mex": "www.scielo.org.mx",
    "per": "www.scielo.org.pe",
    "prt": "www.scielo.oces.mctes.pt",
    "sza": "scielo.za",
    "ury": "www.scielo.edu.uy",
    "ven": "www.scielo.org.ve",
    "spa": "www.scielosp.org"
}

cil = []

# SciELO Collections
for k, v in accounts.items():
    print(k)

    data = {}

    data['collection'] = k
    data['account'] = v
    data['issns'] = []

    query = models.Scielo.objects.filter(collection=k)

    for journal in query:

        data['issns'].append(journal.issn_scielo)

    cil.append(data)

with open('output/collection_issn_account_list.py', 'w') as arquivo:
    pprint(cil, stream=arquivo)

    pprint(cil[1])
