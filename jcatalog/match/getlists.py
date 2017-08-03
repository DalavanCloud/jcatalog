# coding: utf-8
'''
This script get lists from SciELO collection.
'''
import os 
import sys

PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

from proc import models


class Scielo(object):
    # return a list of ISSNs
    def issn_list(self):
        issn_list = []
        for doc in models.Scielo.objects:
            for issn in doc.issn_list:
                issn_list.append(issn)
        
        return issn_list
    

    # return a list of journal titles
    def title_list(self):
        title_list = []
        for doc in models.Scielo.objects:
            title_list.append(doc.title_at_scielo)
        
        return title_list
