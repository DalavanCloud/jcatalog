# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import pyexcel
import logging
import json
import models

from transform_date import *
from accent_remover import *

logging.basicConfig(
    filename='logs/avalicacao-contatos.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


def avaliacao(filename):
    aval = pyexcel.get_sheet(
        file_name=filename,
        sheet_name='import',
        name_columns_by_row=0)

    aval_json = aval.to_records()

    for rec in aval_json:

        # # remove empty keys
        # rec = {k: v for k, v in rec.items() if v or v == 0}
        query = models.Scielo.objects.filter(issn_list=rec['issn'])

        if len(query) == 1 and 'avaliacao' not in query[0]:

            print(rec['issn'])

            doc = query[0]

            data = {'avaliacao': ''}

            contatos = []
            contato = {}
            for k in [
                'email_address',
                'cargo',
                'first_name',
                'last_name',
                'cv_lattes_editor_chefe',
                'aff_editor_chefe',
                'orcid_editor_chefe',
                'email_editor'
            ]:
                if k in rec:
                    contato[k] = rec[k]

            contatos.append(contato)

            data['avaliacao'] = dict(rec)
            data['avaliacao']['contatos'] = contatos

            if data:
                doc.modify(**data)
        else:
            if len(query) == 1:

                print(rec['issn'])

                doc = query[0]

                data = {'avaliacao': ''}

                data['avaliacao'] = json.loads(query[0].to_json())['avaliacao']

                contatos = []
                contato = {}
                for k in [
                    'email_address',
                    'cargo',
                    'first_name',
                    'last_name',
                    'cv_lattes_editor_chefe',
                    'aff_editor_chefe',
                    'orcid_editor_chefe',
                    'email_editor'
                ]:
                    if k in rec:
                        contato[k] = rec[k]

                contatos.append(contato)

                data['avaliacao']['contatos'] = contatos

                if data:
                    doc.modify(**data)


def main():
    # SciELO avaliacao xlsx
    avaliacao('data/scielo/avaliacao/editores-chefes.xlsx')


if __name__ == "__main__":
    main()
