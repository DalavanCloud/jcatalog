# coding: utf-8
'''
This script downloads all Scimago data in XLS format.
Also adds the columns 'Region'; 'Year' and 'Activate (1)'.
'''
import os
import sys
import time
import wget
import logging


PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(filename='logs/extractors.scimago.info.txt',level=logging.INFO)
logger = logging.getLogger(__name__)


def downloader(scielo):

    regions = [
        'Africa',
        'Asiatic Region',
        'Eastern Europe',
        'Latin America',
        'Middle East',
        'Northern America',
        'Pacific Region',
        'Western Europe']

    download_dir = 'data/scimago/xlsx'

    if scielo == 'true':
        if not os.path.exists(download_dir + '/inscielo'):
            os.makedirs(download_dir + '/inscielo')
            os.chdir(download_dir + '/inscielo')
        else:
            os.chdir(download_dir)
    else:
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            os.chdir(download_dir)
        else:
            os.chdir(download_dir)

    for region in regions:

        initial_year = 1999

        last_year = 2017

        while (initial_year <= last_year):

            url = 'http://www.scimagojr.com/journalrank.php'

            link = '%s?year=%s&country=%s&scielo=%s&out=xls' % (
                url,
                str(initial_year),
                region.replace(' ', '%20'),
                scielo)

            filename = wget.download(link)

            if scielo == 'true':
                newfile = 'scimago_' + region.replace(' ', '_') + '_' + str(initial_year) + '_scielo' +'.xlsx'
            else:
                newfile = 'scimago_' + region.replace(' ', '_') + '_' + str(initial_year) + '.xlsx'

            os.rename(filename, newfile)

            msg = '|%s|%s|%s|%s' % (region, str(initial_year), newfile, link)
            logger.info(msg)
            print(msg)

            initial_year += 1

            time.sleep(3)


def main():
    downloader('false')
    os.chdir(PROJECT_PATH)
    downloader('true')


if __name__ == "__main__":
    main()
