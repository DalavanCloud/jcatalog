# coding: utf-8
'''
This script perform data matching from SciELO journals with other sources.
'''
import os 
import sys
import logging
import getlists
import json

PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename='logs/cwts.info.txt',level=logging.INFO)
logger = logging.getLogger(__name__)


from proc import models


def main():
    for issn in getlists.Scielo().issn_list():
        try:
            mat = json.loads(models.Cwts.objects.get(issn_list=issn).to_json())
            print(issn + ': '+ mat['source_title'])
        except models.Cwts.DoesNotExist:
            pass


if __name__ == "__main__":
    main()
