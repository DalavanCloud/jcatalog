# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import pyexcel
import logging
import models

from transform_date import *
from accent_remover import *

logging.basicConfig(filename='logs/toform.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


def toform(filename):
    form = pyexcel.get_sheet(
        file_name=filename,
        sheet_name='SciELO-todos',
        name_columns_by_row=0)

    form_json = form.to_records()

    for rec in form_json:
        print(rec['issn'] + '-' + str(rec['ano_publicação']))
        # remove empty keys
        # rec = {k: v for k, v in rec.items() if v or v == 0}

        year = rec['ano_publicação']

        query = models.Scielo.objects.filter(
            issn_list=rec['issn'],
            activethisyear_inclusion_before=2016)

        # if len(query) == 1 and 'form' not in query[0]:
        data = {}

        if len(query) == 1:
            if year == 2015:
                data['form'] = {'issn': rec['issn']}
                data['form'][str(year)] = {}
                for criterio in [
                        '3-e1',
                        '3-e2',
                        '3-e3',
                        '3-e4',
                        '3-f1',
                        '3-f2']:
                    if criterio in rec and rec[criterio] != "":
                        data['form'][str(year)].update({criterio: rec[criterio]})

            if year == 2017:
                data['form'] = dict(query[0]['form'])
                data['form'][str(year)] = {}
                for criterio in [
                        '3-g1',
                        '3-g2',
                        '3-g3',
                        '3-g4',
                        '3-j0',
                        '3-j1',
                        '3-j2',
                        '3-j3',
                        '4-d',
                        '4-f1',
                        '4-f2']:
                    if criterio in rec and rec[criterio] != "":
                        data['form'][str(year)].update({criterio: rec[criterio]})

            if data:
                print(data)
                query[0].modify(**data)


def main():
    # SciELO avaliacao xlsx
    toform(
        'data/scielo/Fapesp-avaliação-SciELO-todos-20180619-form-a1.xlsx')


if __name__ == "__main__":
    main()
