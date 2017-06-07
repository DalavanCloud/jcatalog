# coding: utf-8

import xlsxwriter
import headers
import models
import sys


def jcatalog():
    
    # Cria a pasta Excel e adiciona uma planilha.
    workbook = xlsxwriter.Workbook('journals_catalog.xlsx')
    worksheet = workbook.add_worksheet('SciELO Journals Catalog')

    # Header
    col = 0
    
    wrap = workbook.add_format({'text_wrap': True})

    for h in headers.scielo_headers:
        worksheet.write(0, col, h, wrap)
        col += 1

    # Extraction date - get date from SciELO collection
    extraction_date = models.Scielo.objects.first().extraction_date
    format_date = workbook.add_format({'num_format': 'dd/mm/yyyy'})

    # SciELO
    row = 1
    scielodocs = models.Scielo.objects()

    for doc in scielodocs:

        col = 0

        worksheet.write_datetime(row, col, extraction_date, format_date)
        col += 1

        # SciELO ou Scopus ou WoS
        if doc.is_scielo == 1 or doc.is_scopus == 1 or doc.is_wos == 1:
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1
        
        # is SciELO
        worksheet.write(row, col, doc.is_scielo); col += 1
        
        # is Scopus
        worksheet.write(row, col, doc.is_scopus); col += 1

        # is WoS
        worksheet.write(row, col, doc.is_wos); col += 1

        # SciELO, Scopus e WoS
        if doc.is_scielo == 1 and doc.is_scopus == 1 and doc.is_wos == 1:
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        # SciELO e Scopus
        if doc.is_scielo == 1 and doc.is_scopus ==1:
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        # SciELO e WoS
        if doc.is_scielo == 1 and doc.is_wos ==1:
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        # Scopus e WoS
        if doc.is_scopus == 1 and doc.is_wos ==1:
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1
 
        # SciELO ou Scopus
        if doc.is_scielo == 1 or doc.is_scopus ==1:
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        # Scopus ou WoS
        if doc.is_scopus == 1 or doc.is_wos ==1:
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        # SciELO ou WoS
        if doc.is_scielo == 1 or doc.is_wos ==1:
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        # SciELO e (Scopus ou WoS)
        if doc.is_scielo == 1 and (doc.is_scopus ==1 or doc.is_wos ==1):
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1
 
        # SciELO e não (Scopus)
        if doc.is_scielo == 1 and doc.is_scopus == 0:
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        # (Scopus ou WoS) e não SciELO
        if (doc.is_scopus == 1 or doc.is_wos == 1) and doc.is_scielo==0:
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        # titulo
        col = 15
        worksheet.write(row, col, doc.title_at_scielo)
        col += 1
        
        # ISSNs
        col = 16
        issns = []
        for i in doc.issns:
            if issns:
                issns = issns + ',' + i
            else:
                issns = i
        if issns:
            worksheet.write(row, col, issns)
        col += 1

        # Issn SciELO
        worksheet.write(row, col, doc.issn_scielo)
        col += 1

        # status
        col = 18
        if doc.title_current_status == 'current':
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1
       

        # Thematic Areas
        worksheet.write(row, col, doc.title_thematic_areas)
        col += 1
        
        if hasattr(doc, 'title_is_agricultural_sciences'):
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        if hasattr(doc, 'title_is_applied_social_sciences'):
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        if hasattr(doc, 'title_is_biological_sciences'):
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        if hasattr(doc, 'title_is_engineering'):
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        if hasattr(doc, 'title_is_exact_and_earth_sciences'):
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        if hasattr(doc, 'title_is_health_sciences'):
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        if hasattr(doc, 'title_is_human_sciences'):
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1
        
        if hasattr(doc, 'title_is_linguistics_letters_and_arts'):
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        if hasattr(doc, 'title_is_multidisciplinary'):
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1

        #Years
        if hasattr(doc, 'inclusion_year_at_scielo'):
            worksheet.write(row, col, doc.inclusion_year_at_scielo)
        else:
            worksheet.write(row, col, '')
        col += 1

        if hasattr(doc, 'stopping_year_at_scielo'):
            worksheet.write(row, col, doc.stopping_year_at_scielo)
        else:
            worksheet.write(row, col, '')
        col += 1


        # Submissions
        worksheet.write(row, col, doc.scholarone)
        col += 1
        
        if hasattr(doc, 'ojs_scielo') or hasattr(doc, 'ojs_outro'):
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1
        
        if hasattr(doc, 'outro'):
            worksheet.write(row, col, 1)
        else:
            worksheet.write(row, col, 0)
        col += 1


        # Google H5 M5
        if hasattr(doc, 'google_scholar_h5_2016'):
            worksheet.write_number(row, col, doc.google_scholar_h5_2016)
        col += 1

        if hasattr(doc, 'google_scholar_m5_2016'):
            worksheet.write_number(row, col, doc.google_scholar_m5_2016)
        col += 1
        

        # DOAJ
        col = 36
        if doc.is_doaj == 1:  
            doaj = models.Doajapi.objects(id=str(doc.doaj_id))[0]
            worksheet.write_number(row, col, 1)
            col += 1
            worksheet.write(row, col, doaj.results[0]['bibjson']['title'])
            col += 1
        else:
            worksheet.write_number(row, col, 0)
            col += 1


        # Scopus
        col = 38
        if doc.is_scopus == 1:
            try:
                docscopus = models.Scopus.objects(id=str(doc.scopus_id))[0]

                if hasattr(docscopus, 'source_title'):
                    worksheet.write(row, col, docscopus.source_title)
                col += 1

                if hasattr(docscopus, 'publishers_name'):
                    worksheet.write(row, col, docscopus.publishers_name)
                col += 1

                if hasattr(docscopus, 'all_science_classification_codes_asjc'):
                    worksheet.write(row, col, docscopus.all_science_classification_codes_asjc)
                col += 1

                if hasattr(docscopus, 'coverage'):
                    worksheet.write(row, col, docscopus.coverage)
                col += 1

                if hasattr(docscopus, 'top_level_life_sciences'):
                    worksheet.write(row, col, docscopus.top_level_life_sciences)
                col += 1

                if hasattr(docscopus, 'top_level_social_sciences'):
                    worksheet.write(row, col, docscopus.top_level_social_sciences)
                col += 1

                if hasattr(docscopus, 'top_level_physical_sciences'):
                    worksheet.write(row, col, docscopus.top_level_physical_sciences)
                col += 1

                if hasattr(docscopus, 'top_level_health_sciences'):
                    worksheet.write(row, col, docscopus.top_level_health_sciences)
                col += 1

                if hasattr(docscopus, 'i1000_general'):
                    worksheet.write(row, col, docscopus.i1000_general)
                col += 1

                if hasattr(docscopus, 'i1100_agricultural_and_biological_sciences'):
                    worksheet.write(row, col, docscopus.i1100_agricultural_and_biological_sciences)
                col += 1

                if hasattr(docscopus, 'i1200_arts_and_humanities'):
                    worksheet.write(row, col, docscopus.i1200_arts_and_humanities)
                col += 1

                if hasattr(docscopus, 'i1300_biochemistry_genetics_and_molecular_biology'):
                    worksheet.write(row, col, docscopus.i1300_biochemistry_genetics_and_molecular_biology)
                col += 1

                if hasattr(docscopus, 'i1400_business_management_and_accounting'):
                    worksheet.write(row, col, docscopus.i1400_business_management_and_accounting)
                col += 1

                if hasattr(docscopus, 'i1500_chemical_engineering'):
                    worksheet.write(row, col, docscopus.i1500_chemical_engineering)
                col += 1

                if hasattr(docscopus, 'i1600_chemistry'):
                    worksheet.write(row, col, docscopus.i1600_chemistry)
                col += 1

                if hasattr(docscopus, 'i1700_computer_science'):
                    worksheet.write(row, col, docscopus.i1700_computer_science)
                col += 1

                if hasattr(docscopus, 'i1800_decision_sciences'):
                    worksheet.write(row, col, docscopus.i1800_decision_sciences)
                col += 1

                if hasattr(docscopus, 'i1900_earth_and_planetary_sciences'):
                    worksheet.write(row, col, docscopus.i1900_earth_and_planetary_sciences)
                col += 1

                if hasattr(docscopus, 'i2000_economics_econometrics_and_finance'):
                    worksheet.write(row, col, docscopus.i2000_economics_econometrics_and_finance)
                col += 1

                if hasattr(docscopus, 'i2100_energy'):
                    worksheet.write(row, col, docscopus.i2100_energy)
                col += 1

                if hasattr(docscopus, 'i2200_engineering'):
                    worksheet.write(row, col, docscopus.i2200_engineering)
                col += 1

                if hasattr(docscopus, 'i2300_environmental_science'):
                    worksheet.write(row, col, docscopus.i2300_environmental_science)
                col += 1

                if hasattr(docscopus, 'i2400_immunology_and_microbiology'):
                    worksheet.write(row, col, docscopus.i2400_immunology_and_microbiology)
                col += 1

                if hasattr(docscopus, 'i2500_materials_science'):
                    worksheet.write(row, col, docscopus.i2500_materials_science)
                col += 1

                if hasattr(docscopus, 'i2600_mathematics'):
                    worksheet.write(row, col, docscopus.i2600_mathematics)
                col += 1

                if hasattr(docscopus, 'i2700_medicine'):
                    worksheet.write(row, col, docscopus.i2700_medicine)
                col += 1

                if hasattr(docscopus, 'i2800_neuroscience'):
                    worksheet.write(row, col, docscopus.i2800_neuroscience)
                col += 1

                if hasattr(docscopus, 'i2900_nursing'):
                    worksheet.write(row, col, docscopus.i2900_nursing)
                col += 1

                if hasattr(docscopus, 'i3000_pharmacology_toxicology_and_pharmaceutics'):
                    worksheet.write(row, col, docscopus.i3000_pharmacology_toxicology_and_pharmaceutics)
                col += 1

                if hasattr(docscopus, 'i3100_physics_and_astronomy'):
                    worksheet.write(row, col, docscopus.i3100_physics_and_astronomy)
                col += 1

                if hasattr(docscopus, 'i3200_psychology'):
                    worksheet.write(row, col, docscopus.i3200_psychology)
                col += 1

                if hasattr(docscopus, 'i3300_social_sciences'):
                    worksheet.write(row, col, docscopus.i3300_social_sciences)
                col += 1

                if hasattr(docscopus, 'i3400_veterinary'):
                    worksheet.write(row, col, docscopus.i3400_veterinary)
                col += 1

                if hasattr(docscopus, 'i3500_dentistry'):
                    worksheet.write(row, col, docscopus.i3500_dentistry)
                col += 1

                if hasattr(docscopus, 'i3600_health_professions'):
                    worksheet.write(row, col, docscopus.i3600_health_professions)
                col += 1

                if hasattr(docscopus, 'i2013_citescore'):
                    worksheet.write(row, col, docscopus.i2013_citescore)
                col += 1

                if hasattr(docscopus, 'i2013_sjr'):
                    worksheet.write(row, col, docscopus.i2013_sjr)
                col += 1

                if hasattr(docscopus, 'i2013_snip'):
                    worksheet.write(row, col, docscopus.i2013_snip)
                col += 1

                if hasattr(docscopus, 'i2014_citescore'):
                    worksheet.write(row, col, docscopus.i2014_citescore)
                col += 1

                if hasattr(docscopus, 'i2014_sjr'):
                    worksheet.write(row, col, docscopus.i2014_sjr)
                col += 1

                if hasattr(docscopus, 'i2014_snip'):
                    worksheet.write(row, col, docscopus.i2014_snip)
                col += 1

                if hasattr(docscopus, 'i2015_citescore'):
                    worksheet.write(row, col, docscopus.i2015_citescore)
                col += 1

                if hasattr(docscopus, 'i2015_sjr'):
                    worksheet.write(row, col, docscopus.i2015_sjr)
                col += 1

                if hasattr(docscopus, 'i2015_snip'):
                    worksheet.write(row, col, docscopus.i2015_snip)
            except:
                pass


        #Scimago
        col = 82
        if doc.is_scimago == 1:
            try:
                docsmago = models.Scimago.objects(id=str(doc.scimago_id))[0]

                if hasattr(docsmago, 'title'):
                    worksheet.write(row, col, docsmago.title)
                col += 1

                if hasattr(docsmago, 'i2013_active'):
                    worksheet.write(row, col, docsmago.i2013_active)
                col += 1

                if hasattr(docsmago, 'i2013_sjr'):
                    worksheet.write(row, col, docsmago.i2013_sjr)
                col += 1

                if hasattr(docsmago, 'i2013_sjr_best_quartile'):
                    worksheet.write(row, col, docsmago.i2013_sjr_best_quartile)
                col += 1

                if hasattr(docsmago, 'i2013_h_index'):
                    worksheet.write(row, col, docsmago.i2013_h_index)
                col += 1

                if hasattr(docsmago, 'i2013_total_docs_2015'):
                    worksheet.write(row, col, docsmago.i2013_total_docs_2015)
                col += 1

                if hasattr(docsmago, 'i2013_total_docs_3years'):
                    worksheet.write(row, col, docsmago.i2013_total_docs_3years)
                col += 1

                if hasattr(docsmago, 'i2013_total_refs'):
                    worksheet.write_number(row, col, docsmago.i2013_total_refs)
                col += 1

                if hasattr(docsmago, 'i2013_total_cites_3years'):
                    worksheet.write_number(row, col, docsmago.i2013_total_cites_3years)
                col += 1

                if hasattr(docsmago, 'i2013_citable_docs_3years'):
                    worksheet.write_number(row, col, docsmago.i2013_citable_docs_3years)
                col += 1

                if hasattr(docsmago, 'i2013_cites_doc_2years'):
                    worksheet.write_number(row, col, docsmago.i2013_cites_doc_2years)
                col += 1

                if hasattr(docsmago, 'i2013_ref_doc'):
                    worksheet.write_number(row, col, docsmago.i2013_ref_doc)
                col += 1

                if hasattr(docsmago, 'i2014_active'):
                    worksheet.write_number(row, col, docsmago.i2014_active)
                col += 1

                if hasattr(docsmago, 'i2014_sjr'):
                    worksheet.write_number(row, col, docsmago.i2014_sjr)
                col += 1
                
                if hasattr(docsmago, 'i2014_sjr_best_quartile'):
                    worksheet.write(row, col, docsmago.i2014_sjr_best_quartile)
                col += 1

                if hasattr(docsmago, 'i2014_h_index'):
                    worksheet.write_number(row, col, docsmago.i2014_h_index)
                col += 1

                if hasattr(docsmago, 'i2014_total_docs_2015'):
                    worksheet.write_number(row, col, docsmago.i2014_total_docs_2015)
                col += 1

                if hasattr(docsmago, 'i2014_total_docs_3years'):
                    worksheet.write_number(row, col, docsmago.i2014_total_docs_3years)
                col += 1

                if hasattr(docsmago, 'i2014_total_refs'):
                    worksheet.write_number(row, col, docsmago.i2014_total_refs)
                col += 1

                if hasattr(docsmago, 'i2014_total_cites_3years'):
                    worksheet.write_number(row, col, docsmago.i2014_total_cites_3years)
                col += 1

                if hasattr(docsmago, 'i2014_citable_docs_3years'):
                    worksheet.write_number(row, col, docsmago.i2014_citable_docs_3years)
                col += 1

                if hasattr(docsmago, 'i2014_cites_doc_2years'):
                    worksheet.write_number(row, col, docsmago.i2014_cites_doc_2years)
                col += 1

                if hasattr(docsmago, 'i2014_ref_doc'):
                    worksheet.write_number(row, col, docsmago.i2014_ref_doc)
                col += 1

                if hasattr(docsmago, 'i2015_active'):
                    worksheet.write_number(row, col, docsmago.i2015_active)
                col += 1

                if hasattr(docsmago, 'i2015_sjr'):
                    worksheet.write_number(row, col, docsmago.i2015_sjr)
                col += 1

                if hasattr(docsmago, 'i2015_sjr_best_quartile'):
                    worksheet.write(row, col, docsmago.i2015_sjr_best_quartile)
                col += 1

                if hasattr(docsmago, 'i2015_h_index'):
                    worksheet.write_number(row, col, docsmago.i2015_h_index)
                col += 1

                if hasattr(docsmago, 'i2015_total_docs_2015'):
                    worksheet.write_number(row, col, docsmago.i2015_total_docs_2015)
                col += 1

                if hasattr(docsmago, 'i2015_total_docs_3years'):
                    worksheet.write_number(row, col, docsmago.i2015_total_docs_3years)
                col += 1

                if hasattr(docsmago, 'i2015_total_refs'):
                    worksheet.write_number(row, col, docsmago.i2015_total_refs)
                col += 1

                if hasattr(docsmago, 'i2015_total_cites_3years'):
                    worksheet.write_number(row, col, docsmago.i2015_total_cites_3years)
                col += 1

                if hasattr(docsmago, 'i2015_citable_docs_3years'):
                    worksheet.write_number(row, col, docsmago.i2015_citable_docs_3years)
                col += 1

                if hasattr(docsmago, 'i2015_cites_doc_2years'):
                    worksheet.write_number(row, col, docsmago.i2015_cites_doc_2years)
                col += 1

                if hasattr(docsmago, 'i2015_ref_doc'):
                    worksheet.write_number(row, col, docsmago.i2015_ref_doc)
                col += 1
            except:
                pass
        
        # WOS
        col = 116
        #ind = workbook.add_format({'num_format': '0.000'})
        if doc.is_wos == 1:
            try:
                docwos = models.Wos.objects(id=str(doc.wos_id))[0]
                
                if hasattr(docwos, 'total_cites'):
                    worksheet.write(row, col, docwos.total_cites)
                col += 1

                if hasattr(docwos, 'journal_impact_factor'):
                    worksheet.write(row, col, docwos.journal_impact_factor)
                col += 1

                if hasattr(docwos, 'impact_factor_without_journal_self_cites'):
                    worksheet.write(row, col, docwos.impact_factor_without_journal_self_cites)
                col += 1

                if hasattr(docwos, 'five_year_impact_factor'):
                    worksheet.write(row, col, docwos.five_year_impact_factor)
                col += 1

                if hasattr(docwos, 'immediacy_index'):
                    worksheet.write(row, col, docwos.immediacy_index)
                col += 1

                if hasattr(docwos, 'citable_items'):
                    worksheet.write(row, col, docwos.citable_items)
                col += 1

                if hasattr(docwos, 'cited_half_life'):
                    worksheet.write(row, col, docwos.cited_half_life)
                col += 1

                if hasattr(docwos, 'citing_half_life'):
                    worksheet.write(row, col, docwos.citing_half_life)
                col += 1

                if hasattr(docwos, 'eigenfactor_score'):
                    worksheet.write(row, col, docwos.eigenfactor_score)
                col += 1

                if hasattr(docwos, 'article_influence_score'):
                    worksheet.write(row, col, docwos.article_influence_score)
                col += 1

                if hasattr(docwos, 'percentage_articles_in_citable_items'):
                    worksheet.write(row, col, docwos.percentage_articles_in_citable_items)
                col += 1

                if hasattr(docwos, 'average_journal_impact_factor_percentile'):
                    worksheet.write(row, col, docwos.average_journal_impact_factor_percentile)
                col += 1

                if hasattr(docwos, 'normalized_eigenfactor'):
                    worksheet.write(row, col, docwos.normalized_eigenfactor)
                col += 1
            except:
                pass

        # Avançar linha - prox. documento
        row += 1

    print('número da última linha: %s' % row)


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
