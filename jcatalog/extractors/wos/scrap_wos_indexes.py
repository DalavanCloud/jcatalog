# coding: utf-8
'''
This script is an index scraper from the Master Journal List - Clarivates
'''
import csv
import time
import requests
from bs4 import BeautifulSoup


def scrapmjl(preurl, index, filewriter):

    for page in range(1, 21):
        try:
            url = preurl + "&Page=" + str(page)
            print(url)

            r = requests.get(url)
            time.sleep(2)

            r_html = r.text.replace('\r', '')
            soup = BeautifulSoup(r_html, 'html.parser')
            soupdt = soup.findAll('dt')

            if soupdt:
                for l in soup.findAll('dt'):
                    filewriter.writerow([
                        l.next_sibling.split(' ISSN: ')[1].strip(),
                        l.text.split('. ')[1],
                        l.next_sibling.split(' ISSN: ')[0].strip(),
                        index])
            else:
                break
        except Exception as e:
            print(e)
            break


def main():

    ci_tuple_list = [
        # Arts & Humanities Citation Index
        # PC = 'H'
        ('H', 'ahci'),
        # Science Citation Index Expanded
        # PC = 'D'
        ('D', 'scie'),
        # Social Sciences Citation Index
        # PC = 'SS'
        ('SS', 'ssci'),
        # Emerging Sources Citation Index
        # PC = 'EX'
        ('EX', 'esci'),
        # Science Citation Index
        # PC = 'K'
        ('K', 'sci')]
    '''
    The Science Citation Index (SCI) is a highly selective subset of journals
    found in the Science Citation Index Expanded. Journals in SCI are typically
    the most consistently high impact titles in many scientific disciplines.
    '''
    with open('data/wos/master_journal_list.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter='\t',
                                quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(
            [
                'issn',
                'journal',
                'frequency',
                'index'])

        for code, index in ci_tuple_list:
            preurl = "http://mjl.clarivate.com/cgi-bin/jrnlst/jlresults.cgi?PC=" + code + "&mode=print"
            print(index)
            scrapmjl(preurl, index, filewriter)

if __name__ == '__main__':
    main()
