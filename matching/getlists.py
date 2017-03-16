# coding: utf-8
'''
This script get lists from SciELO collection.
'''
import os 
import sys

PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

from proc import models


class Scielo():
    # return a list of ISSNs
    def issn_list():
        issn_list = []
        for doc in models.Scielo.objects:
            [issn_list.append(issn) for issn in doc.issn_list]
        
        return issn_list
    

    # return a list of journal titles
    def title_list():
        title_list = []
        for doc in models.Scielo.objects:
            title_list.append(doc.title_at_scielo)
        
        return title_list
