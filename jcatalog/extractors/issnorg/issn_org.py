# coding: utf-8
import os
import sys
import logging
import configparser
import json
import time
from ast import literal_eval as make_tuple

from articlemeta.client import ThriftClient
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import models

PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

logging.basicConfig(
    filename='logs/issn_org.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)

# Reads Config
print('Carregando as configurações\n')
config = configparser.ConfigParser()
config.read('extractors/issnorg/config.ini')


def mywebdriver(driver):

    domain = config['DEFAULT']['Domain']

    text_file = open("extractors/issnorg/journalslist.txt", "r")
    lines = text_file.readlines()
    text_file.close()

    for line in lines:

        journal = make_tuple(line)

        # https://portal.issn.org/resource/ISSN/0716-9760?format=json
        url = "%sresource/ISSN/%s?format=json" % (domain, journal[0])
        print(url)

        try:
            driver.get(url)
            wait = WebDriverWait(driver, 10)
            wait.until(EC.element_to_be_clickable((By.ID, 'rawdata-tab')))
            driver.find_element_by_id("rawdata-tab").click()
            rec = json.loads(driver.find_element_by_class_name('data').text)
        except TimeoutException:
            logs = "ERRO|" + journal[0]
            logger.info(logs)
            print(logs)
            continue

        rec['issn_scielo'] = journal[0]
        rec['collection'] = journal[1]
        rec['title'] = journal[2]

        if 'continues' in rec['@graph']:
            # 'resource/ISSN/0004-0533'
            continues = rec['@graph'][2]['continues']
            urlc = "%s%s?format=json" % (domain, continues)
            print(urlc)
            driver.get(urlc)
            wait = WebDriverWait(driver, 10)
            wait.until(EC.element_to_be_clickable((By.ID, 'rawdata-tab')))
            driver.find_element_by_id("rawdata-tab").click()

            jc = json.loads(driver.find_element_by_class_name('data').text)

            rec['related_title']['continues'] = jc['mainTitle']

        # delete key/value with '.' to save in MongoDB
        for d in rec['@graph']:
            for k in list(d.keys()):
                if '.' in k:
                    del d[k]

        # Save in MongoDB
        doc = models.Issnorg(**rec)
        doc.save()

        # log
        logs = journal
        logger.info(logs)


def main():

    # Load ISSN list from Articlemeta
    # client = ThriftClient()

    # # journalslist = [('0716-9760', 'chl', 'br'), ('0074-0276', 'scl', 'mioc')]
    # print("Obtendo lista de ISSNs de ArticleMeta SciELO")
    # print("Aguarde...\n")

    # with open('extractors/issnorg/journalslist.txt', 'w') as f:

    #     for journal in client.journals():
    #         if journal.collection_acronym not in [
    #                 'sss',
    #                 'rve',
    #                 'psi',
    #                 'rvt',
    #                 'ecu']:

    #             f.write('%s\n' % str((journal.scielo_issn,
    #                                   journal.collection_acronym,
    #                                   journal.title)))

    # ISSN.org Login
    print('Abrindo o navegador Firefox')
    print("Aguarde...\n")

    if config['LOGIN']['LoginAccess'] == 'yes':

        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.get(config['DEFAULT']['Domain'])

        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Leave this field blank'])[1]/following::img[1]").click()

        print('Efetuando Login...\n')
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys(
            config['LOGIN']['User'])
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys(config['LOGIN']['Pass'])
        driver.find_element_by_id("submit").click()

        print('Iniciando a navegação\n')

        mywebdriver(driver)

        driver.get("https://portal.issn.org/user/logout")
        driver.close()
    else:
        print("configurar senha")


if __name__ == '__main__':
    main()
