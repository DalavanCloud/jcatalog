# coding: utf-8
'''
TESTE
'''

from tools import data_corrections

# from transform import scopus_loader
# from transform import scopus_update

from transform import wos_country

if __name__ == "__main__":

    data_corrections.scielosp()
    data_corrections.scopus()
    data_corrections.scimago()

    # scopus_loader.main()
    # scopus_update.main()

    wos_country.main()
