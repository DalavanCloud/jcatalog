# coding: utf-8
'''
This script downloads all Scimago data in XLS format.
Also adds the columns 'Region'; 'Year' and 'Activate (1)'.
'''

import os
import sys
import wget
from datetime import date
import time
import logging


PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename='logs/extractors.scimago.info.txt',level=logging.INFO)
logger = logging.getLogger(__name__)


regions = ['Africa', 
    'Asiatic Region', 
    'Eastern Europe', 
    'Latin America', 
    'Middle East', 
    'Northern America', 
    'Pacific Region', 
    'Western Europe']

if not os.path.exists('data/scimago/xlsx'):
    os.makedirs('data/scimago/xlsx')
    os.chdir('data/scimago/xlsx')
else:
    os.chdir('data/scimago/xlsx')

for reg in regions:

    initial_year = 1999

    last_year = date.today().year - 1

    while (initial_year <= last_year):

        url = 'http://www.scimagojr.com/journalrank.php?year='+ str(initial_year) + '&country='+ reg.replace(' ', '%20') +'&out=xls'

        filename = wget.download(url)

        os.rename(filename, 'scimago_' + reg.replace(' ', '_') + '_' + str(initial_year) + '.xlsx')
        
        newfile = 'scimago_' + reg.replace(' ', '_') + '_' + str(initial_year) + '.xlsx'

        msg = '|%s|%s|%s' % (reg, str(initial_year), newfile)
        logger.info(msg)
        print(msg)

        initial_year += 1

        time.sleep(3)
