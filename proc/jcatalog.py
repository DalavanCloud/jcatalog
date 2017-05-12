
# coding: utf-8

import xlsxwriter
import headers
import models
import keycorrection
import operator

def jcatalog():
    
    # Cria a pasta Excel e adiciona um planilha.
    workbook = xlsxwriter.Workbook('journals_catalog.xlsx')
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})
    red = workbook.add_format({'font_color': 'red'})

    # Header
    headers = ['SciELO','Scopus','WoS', 'SciELO, Scopus e WoS',
    'issn_scielo',
    'issns',
    'Título Scielo', 
    'Status na Scielo', 
    'ScholarOne', 
    'OJS', 
    'Acesso Submission', 
    'google_scholar_h5_2016',
    'google_scholar_m5_2016',
    'Título Scopus', 
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

        worksheet.write(row, col, doc.is_scielo); col += 1
        worksheet.write(row, col, doc.is_scopus); col += 1
        worksheet.write(row, col, doc.is_wos); col += 1

        if doc.is_scielo == 1 and doc.is_scopus == 1 and doc.is_wos == 1:
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        worksheet.write(row, col, doc.issn_scielo); col += 1
        
        issns = []
        for i in doc.issns:
            issns.append(i)
        worksheet.write(row, col, str(issns).replace('[','').replace(']','')); col += 1
        
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
            for issn in doc.issn_list:
                try:
                    worksheet.write(row, col, models.Scopus.objects.get(issn_list=issn).source_title)
                except:
                    pass
            col += 1     
            for issn in doc.issn_list:  
                try:
                    worksheet.write(row, col, models.Scopus.objects.get(issn_list=issn).publishers_name)
                except:
                    pass
        else:
            col += 2

        # WOS
        col = 15
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

    worksheet2 = workbook.add_worksheet('WoS')
    
    headers_wos = keycorrection.jcr_columns_names
    
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

    # grava planilha Excel
    try:
        workbook.close()
    except IOError as e:
        print(e)
        sys.exit(1)


def main():
    
    jcatalog()


if __name__ == "__main__":
    main()
