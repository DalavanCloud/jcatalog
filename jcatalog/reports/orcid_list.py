# coding: utf-8
'''
Este script lista os autores que possuem ORCID
1 - faz uma consulta em search.scielo.org por orcid: *
2 - obtem o total de linhas e repete a consulta passando o total de linhas
3 - gera uma lista de tuplas formada por PID e Coleção
4 - consulta em articlemeta os dados do artigo
5 - obtem as datas no mongoDB - coleção Scielodates.
    Scielodates é carregado a partir de documents_dates.csv
'''
import logging
import time
import datetime
import requests
import xlsxwriter

from articlemeta.client import ThriftClient
import models


client = ThriftClient()

logging.basicConfig(filename='logs/orcid_list.info.txt', level=logging.INFO)
logger = logging.getLogger(__name__)

today = datetime.datetime.now().strftime('%Y%m%d')


def getpids(query):
    url = 'http://search.scielo.org:8080/solr/scielo-articles/select?q='+query+'&wt=json&indent=true'
    try:
        r = requests.get(url)
        time.sleep(2)
        if r.status_code == 200:
            docs = r.json()
            rows = str(docs['response']['numFound'])
            print('documentos localizados: %s' % rows)
    except Exception as e:
        print(e)
        raise

    try:
        url2 = 'http://search.scielo.org:8080/solr/scielo-articles/select?q='+query+'&rows='+rows+'&wt=json&indent=true' 
        r = requests.get(url2)
        time.sleep(2)
        if r.status_code == 200:
            pids_list = []
            docs = r.json()
            for j in docs['response']['docs']:
                pids_list.append((j['id'][0:23], j['id'][24:]))
        return pids_list
    except Exception as e:
        print(e)
        raise


def orcid(pid_col_tuples):

    # Cria a pasta Excel e adiciona uma planilha
    workbook = xlsxwriter.Workbook('output/scielo_orcid_authors_'+today+'.xlsx')
    worksheet = workbook.add_worksheet('SciELO - autores com ORCID')

    format_date = workbook.add_format({'num_format': 'yyyy-mm-dd'})

    row = 0
    col = 0

    for h in [
        'data extração',
        'título do periódico',
        'issn_scielo',
        'pid',
        'coleção',
        'pid-coleção',
        'doi',
        'data de submissão',
        'data de aprovação',
        'data de publicação',
        'data de publicação no SciELO',
        'volume',
        'numero',
        'pagina inicial',
        'pagina final',
        'elocation',
        'nome',
        'sobrenome',
        'ORCID',
        'países',
        'países ISO',
        'instituição afiliação 1',
        'instituição afiliação 2',
        'instituição afiliação 3',
        'instituição afiliação 4'
            ]:
        worksheet.write(row, col, h)
        col += 1

    row = 1

    for rec in pid_col_tuples:
        print(rec[0])
        # logger.info(rec['ID'])

        try:
            d = client.document(code=rec[0], collection=rec[1])

            for n, au in enumerate(d.authors):
                col = 0

                d.journal.scielo_issn
                worksheet.write(row, col, today, format_date)
                col += 1
                worksheet.write(row, col, d.journal.title)
                col += 1
                worksheet.write(row, col, d.journal.scielo_issn)
                col += 1
                worksheet.write(row, col, d.publisher_id)
                col += 1
                worksheet.write(row, col, d.collection_acronym)
                col += 1
                worksheet.write(row, col, rec[0])
                col += 1
                worksheet.write(row, col, d.doi)
                col += 1

                query = models.Scielodates.objects.filter(
                    pid=d.publisher_id,
                    collection=d.collection_acronym)

                if query:
                    doc = query[0]

                    if 'document_submitted_at' in doc:
                        worksheet.write(row, col, doc['document_submitted_at'])
                    col += 1

                    if 'document_accepted_at' in doc:
                        worksheet.write(row, col, doc['document_accepted_at'])
                    col += 1

                    if 'document_published_at' in doc:
                        worksheet.write(row, col, doc['document_published_at'])
                    col += 1
                    if 'document_published_in_scielo_at' in doc:
                        worksheet.write(row, col, doc['document_published_in_scielo_at'])
                    col += 1
                else:
                    col += 4

                worksheet.write(row, col, d.issue.volume)
                col += 1
                worksheet.write(row, col, d.issue.number)
                col += 1
                if hasattr(d, 'start_page'):
                    worksheet.write(row, col, d.start_page)
                col += 1
                if hasattr(d, 'end_page'):
                    worksheet.write(row, col, d.end_page)
                col += 1
                worksheet.write(row, col, d.elocation)
                col += 1
                worksheet.write(row, col, au['given_names'])
                col += 1
                worksheet.write(row, col, au['surname'])
                col += 1
                if 'orcid' in au:
                    worksheet.write(row, col, au['orcid'])
                col += 1

                # Countries
                countries = []
                if 'xref' in au:
                    for xref in au['xref']:
                        for aff in d.affiliations:
                            if aff['index'].lower() == xref:
                                if aff['country'] not in countries:
                                    countries.append(aff['country'])
                if countries:
                    worksheet.write(row, col, '; '.join([c for c in countries]))
                col += 1

                # Countries ISO
                countries_iso = []
                if 'xref' in au:
                    for xref in au['xref']:
                        for aff in d.affiliations:
                            if aff['index'].lower() == xref:
                                if aff['country_iso_3166'] not in countries_iso:
                                    countries_iso.append(aff['country_iso_3166'])
                if countries_iso:
                    worksheet.write(row, col, '; '.join([c for c in countries_iso]))
                col += 1

                # Instituições Afiliadas
                if 'xref' in au:
                    for xref in au['xref']:
                        for aff in d.affiliations:
                            if aff['index'].lower() == xref:
                                worksheet.write(row, col, aff['institution'])
                                col += 1

                row += 1
        except Exception as e:
            logger.info(e)
            logger.info('not find in articlemeta')
            print(e)


def main():

    query = 'orcid%3A*'

    pid_col_tuples = getpids(query)

    orcid(pid_col_tuples)

if __name__ == '__main__':
    main()
