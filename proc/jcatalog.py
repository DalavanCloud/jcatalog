# coding: utf-8

import xlsxwriter
import headers
import models
import keycorrection
import operator

def jcatalog():
    
    # Cria a pasta Excel e adiciona um planilha.
    workbook = xlsxwriter.Workbook('journals_catalog.xlsx')
    worksheet = workbook.add_worksheet('SciELO Brazil')

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})
    red = workbook.add_format({'font_color': 'red'})

    # Header
    headers = ['SciELO or Scopus or WoS'
    'SciELO',
    'Scopus',
    'WoS', 
    'SciELO, Scopus e WoS',
    'SciELO issn',
    'SciELO issns',
    'Title at SciELO', 
    'Status at SciELO', 
    'ScholarOne', 
    'OJS', 
    'Submission access', 
    'google_scholar_h5_2016',
    'google_scholar_m5_2016',
    'Scopus title', 
    'Scopus publisher', 
    'WoS Impact Factor',
    'WoS 5 year Impact Factor',
    'WoS Immediacy Index']
    
    col = 0
    
    for h in headers:
        worksheet.write(0, col, h, bold)
        col += 1

    # SciELO
    row = 1
    scielodocs = models.Scielo.objects()

    for doc in scielodocs:

        col = 0
        
        if doc.is_scielo == 1 or doc.is_scopus == 1 or doc.is_wos == 1:
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        worksheet.write(row, col, doc.is_scielo); col += 1
        worksheet.write(row, col, doc.is_scopus); col += 1
        worksheet.write(row, col, doc.is_wos); col += 1

        if doc.is_scielo == 1 and doc.is_scopus == 1 and doc.is_wos == 1:
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        worksheet.write(row, col, doc.issn_scielo); col += 1
        
        # issns       
        issns = []
        for i in doc.issns:
            if issns:
                issns = issns + ',' + i
            else:
                issns = i
        if issns:
            worksheet.write(row, col, issns)
        col += 1
        
        worksheet.write(row, col, doc.title_at_scielo); col += 1
        worksheet.write(row, col, doc.title_current_status); col += 1

        # submissions
        worksheet.write(row, col, doc.scholarone); col += 1
        worksheet.write(row, col, doc.ojs_scielo); col += 1

        # Submissions - acesso
        for issn in doc.issn_list:
            try:
                acesso = models.Submissions.objects.get(issn_scielo=issn).endereco_acesso
                worksheet.write(row, col, acesso).endereco_acesso
            except:
                pass
        
        col += 1

        # google
        if hasattr(doc, 'google_scholar_h5_2016'):
            worksheet.write(row, col, doc.google_scholar_h5_2016); col += 1
            worksheet.write(row, col, doc.google_scholar_m5_2016); col += 1
        else:
            col += 2

        # Scopus
        if doc.is_scopus == 1:
            try:
                docscopus = models.Scopus.objects(id=str(doc.scopus_id))[0]

                if hasattr(docscopus, 'source_title'):
                    worksheet.write(row, col, docscopus.source_title)
                col += 1

                if hasattr(docscopus, 'publishers_name'):
                    worksheet.write(row, col, docscopus.publishers_name)
                col += 1

            except:
                pass
        else:
            col += 2 # (Se não é Scopus, força o avanço de 2 colunas)


        # WOS
        col = 16
        ind = workbook.add_format({'num_format': '#.###'})
        if doc.is_wos == 1:
            try:
                doc_wos = models.Wos.objects(id=str(doc.wos_id))[0]
                worksheet.write(row, col, str(doc_wos.journal_impact_factor), ind); col += 1
                worksheet.write(row, col, str(doc_wos.five_year_impact_factor), ind); col += 1
                worksheet.write(row, col, str(doc_wos.immediacy_index), ind); col += 1
            except:
                pass

        # Avançar linha - prox. documento       
        row += 1

    print('número da última linha: %s' % row)
    

    # WOS completo

    worksheet2 = workbook.add_worksheet('WoS_completo')
    
    headers_wos = keycorrection.wos_columns_names
    
    col = 0
    for h in headers_wos:
        worksheet2.write(0, col, h, red)
        col += 1

    # Start from the first cell below the headers.
    row = 1
    
    # Iterate over the data and write it out row by row.
    for doc in models.Wos.objects():
        col = 0
        for h in headers_wos:
            if h in doc:
                worksheet2.write(row, col, operator.attrgetter(h)(doc))
                col += 1
            else:
                col +=1
        row += 1


    # Outras fontes

    list_titles = []
    
    # Scimago = 140
    worksheet3 = workbook.add_worksheet('Scimago')
    row = 0
    #for doc in models.Scimago.objects.filter(country='Brazil', is_scielo=0, is_wos=0, is_scopus=1):
    for doc in models.Scimago.objects.filter(country='Brazil', is_scielo=0):
        worksheet3.write(row, 0, doc.title)
        list_titles.append(doc.title.lower())
        row += 1
    print(models.Scimago.objects.filter(country='Brazil', is_scielo=0).count())

    # Scopus = 187
    worksheet4 = workbook.add_worksheet('Scopus')
    row = 0
    #for doc in models.Scopus.objects.filter(publishers_country='Brazil', is_scielo=0, is_wos=0, is_scimago=1):
    for doc in models.Scopus.objects.filter(publishers_country='Brazil', is_scielo=0):
        worksheet4.write(row, 0, doc.source_title)
        list_titles.append(doc.source_title.lower())
        row += 1
    print(models.Scopus.objects.filter(publishers_country='Brazil', is_scielo=0).count())

    # Wos = 22
    worksheet5 = workbook.add_worksheet('Wos')
    row = 0
    for doc in models.Wos.objects.filter(is_scielo=0):
        worksheet5.write(row, 0, doc.full_journal_title)
        list_titles.append(doc.full_journal_title.lower())
        row += 1
    print(models.Wos.objects.filter(is_scielo=0).count())
    
    # Lista unificada de títulos
    worksheet6 = workbook.add_worksheet('Titulos Unificados')
    row = 0
    # new_list = list(set(list_titles))
    # sorted(new_list)
    for l in sorted(set(list_titles)):
        worksheet6.write(row, 0, l)
        row += 1


    # Grava planilha Excel
    try:
        workbook.close()
    except IOError as e:
        print(e)
        sys.exit(1)


def main():
    
    jcatalog()


if __name__ == "__main__":
    main()
