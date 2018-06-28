# coding: utf-8
'''
Este script apenas demarca os conjuntos de periódicos participantes da
Avaliação FAPESP
'''
import logging
import models

logging.basicConfig(
    filename='logs/fapesp_evaluation.info.txt',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def alljournals(col, year):
    query = models.Scielo.objects.filter(collection=col)
    if query:
        for doc in query:
            if 'fapesp_evaluation' not in doc:
                data = {'fapesp_evaluation': {
                    str(year): {'fullset': 1}
                    }
                }
                doc.modify(**data)
            else:
                doc['fapesp_evaluation'][str(year)] = {'fullset': 1}
                doc.save()


def activethisyear(col, year):
    query = models.Scielo.objects.filter(
        title_current_status='current',
        collection='scl')
    if query:
        for doc in query:
            if 'fapesp_evaluation' not in doc:

                data = {'fapesp_evaluation': {
                    str(year): {
                        'fullset': 1,
                        'activethisyear': 1}
                    }
                }
                doc.modify(**data)
            else:
                doc['fapesp_evaluation'][str(year)] = {
                    'fullset': 1,
                    'activethisyear': 1}
                doc.save()


def activethisyear_inclusion_before(col, year, year_before):
    query = models.Scielo.objects.filter(
        title_current_status='current',
        collection=col)
    counter = 0

    for doc in query:
        docs_year = 0
        inclusion = 0
        ative_year = 0

        if 'docs' in doc:
            if 'docs_'+str(year_before) in doc['docs']:
                if doc['docs']['docs_'+str(year_before)] == '':
                    pass
                elif doc['docs']['docs_'+str(year_before)] > 0:
                    docs_year = 1

                # 2007 ao ano da avaliacao +1
                for y in range(2007, year+1):
                    year_str = str(y)
                    if 'docs_'+year_str in doc['docs']:
                        if doc['docs']['docs_'+year_str] == '':
                            pass
                        elif int(doc['docs']['docs_'+year_str]) > 0:
                            ative_year = 1
                            break

        if doc['inclusion_year_at_scielo'] < year_before:
            inclusion = 1

        if docs_year == 1 and inclusion == 1 and ative_year == 1:
            counter += 1
            doc['fapesp_evaluation'][str(year)] = {
                    'fullset': 1,
                    'activethisyear': 1,
                    'inclusion_before': year_before,
                    'evaluated': 1}
            doc.save()

    print('Evaluated: '+str(counter))


def main():
    # Separa o conjunto de periodicos que fazem parte da avaliação FAPESP

    # Todos os periodicos
    # Informar a colecao e o ano da avaliacao
    alljournals('scl', 2018)

    # Ativos no ano da avaliacao. São os periódicos em status = current
    # inforar a colecao e o ano da avaliacao
    activethisyear('scl', 2018)

    '''
    Periódicos filtrados para a avaliacao conforme os critérios abaixo:
    Informar a colecao, o ano da avaliacao e quando se inicia o ano de inclusao
    Ex.: 2016, serao selecionados os periodicos que foram incluidos na colecao
    SciELO antes de 2016 (de 2015 para tras)
    '''
    activethisyear_inclusion_before('scl', 2018, 2016)


if __name__ == "__main__":
    main()
