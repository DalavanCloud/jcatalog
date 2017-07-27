# coding: utf-8

# SciELO
scielo_columns_names = [
 'extraction_date',
 'study_unit',
 'collection',
 'issn_scielo',
 'issns',
 'title',
 'title_thematic_areas',
 'title_is_agricultural_sciences',
 'title_is_applied_social_sciences',
 'title_is_biological_sciences',
 'title_is_engineering',
 'title_is_exact_and_earth_sciences',
 'title_is_health_sciences',
 'title_is_human_sciences',
 'title_is_linguistics_letters_and_arts',
 'title_is_multidisciplinary',
 'title_current_status',
 'title_subtitle_scielo',
 'short_title_scielo',
 'short_title_iso',
 'title_pubmed',
 'publisher_name',
 'use_license',
 'alpha_frequency',
 'numeric_frequency_(in_months)',
 'inclusion_year_at_scielo',
 'stopping_year_at_scielo',
 'stopping_reason',
 'date_of_the_first_document',
 'volume_of_the_first_document',
 'issue_of_the_first_document',
 'date_of_the_last_document',
 'volume_of_the_last_document',
 'issue_of_the_last_document',
 'total_of_issues',
 'issues_at_2017',
 'issues_at_2016',
 'issues_at_2015',
 'issues_at_2014',
 'issues_at_2013',
 'issues_at_2012',
 'total_of_regular_issues',
 'regular_issues_at_2017',
 'regular_issues_at_2016',
 'regular_issues_at_2015',
 'regular_issues_at_2014',
 'regular_issues_at_2013',
 'regular_issues_at_2012',
 'total_of_documents',
 'documents_at_2017',
 'documents_at_2016',
 'documents_at_2015',
 'documents_at_2014',
 'documents_at_2013',
 'documents_at_2012',
 'citable_documents',
 'citable_documents_at_2017',
 'citable_documents_at_2016',
 'citable_documents_at_2015',
 'citable_documents_at_2014',
 'citable_documents_at_2013',
 'citable_documents_at_2012',
 'portuguese_documents_at_2017',
 'portuguese_documents_at_2016',
 'portuguese_documents_at_2015',
 'portuguese_documents_at_2014',
 'portuguese_documents_at_2013',
 'portuguese_documents_at_2012',
 'spanish_documents_at_2017',
 'spanish_documents_at_2016',
 'spanish_documents_at_2015',
 'spanish_documents_at_2014',
 'spanish_documents_at_2013',
 'spanish_documents_at_2012',
 'english_documents_at_2017',
 'english_documents_at_2016',
 'english_documents_at_2015',
 'english_documents_at_2014',
 'english_documents_at_2013',
 'english_documents_at_2012',
 'other_language_documents_at_2017',
 'other_language_documents_at_2016',
 'other_language_documents_at_2015',
 'other_language_documents_at_2014',
 'other_language_documents_at_2013',
 'other_language_documents_at_2012',
 'google_scholar_h5_2017',
 'google_scholar_h5_2016',
 'google_scholar_h5_2015',
 'google_scholar_h5_2014',
 'google_scholar_h5_2013',
 'google_scholar_h5_2012',
 'google_scholar_m5_2017',
 'google_scholar_m5_2016',
 'google_scholar_m5_2015',
 'google_scholar_m5_2014',
 'google_scholar_m5_2013',
 'google_scholar_m5_2012']

submission_scielo_brasil_columns_names = [
 'title',
 'data_inclusao_scielo',
 'issn_scielo',
 'scholarone',
 'ojs_scielo',
 'ojs_outro',
 'outro',
 'endereco_acesso']


# Scimago
scimago_columns_names = [
 'rank',
 'title',
 'type',
 'issn',
 'sjr',
 'sjr_best_quartile',
 'h_index',
 'total_docs',
 'total_docs_3years',
 'total_refs',
 'total_cites_3years',
 'citable_docs_3years',
 'cites_by_doc_2years',
 'ref_by_doc',
 'country']

# Scopus
scopus_columns_names_2015 = [
 'sourcerecord_id',
 'title',
 'print_issn',
 'e_issn',
 'active_or_inactive',
 'coverage',
 'article_language_source_iso_codes',
 'citescore_2013',
 'sjr_2013',
 'snip_2013',
 'citescore_2014',
 'sjr_2014',
 'snip_2014',
 'citescore_2015',
 'sjr_2015',
 'snip_2015',
 'medline_sourced_title',
 'open_acces_status',
 'articles_in_press_included',
 'added_to_list_since_october_2016',
 'source_type',
 'title_history_indication',
 'related_title_to_title_history_indication',
 'other_related_title_1',
 'other_related_title_2',
 'other_related_title_3',
 'publishers_name',
 'publisher_imprints_grouped_to_main_publisher',
 'publishers_country',
 'all_science_classification_codes_asjc',
 'top_level_life_sciences',
 'top_level_social_sciences',
 'top_level_physical_sciences',
 'top_level_health_sciences',
 'c1000_general',
 'c1100_agricultural_and_biological_sciences',
 'c1200_arts_and_humanities',
 'c1300_biochemistry_genetics_and_molecular_biology',
 'c1400_business_management_and_accounting',
 'c1500_chemical_engineering',
 'c1600_chemistry',
 'c1700_computer_science',
 'c1800_decision_sciences',
 'c1900_earth_and_planetary_sciences',
 'c2000_economics_econometrics_and_finance',
 'c2100_energy',
 'c2200_engineering',
 'c2300_environmental_science',
 'c2400_immunology_and_microbiology',
 'c2500_materials_science',
 'c2600_mathematics',
 'c2700_medicine',
 'c2800_neuroscience',
 'c2900_nursing',
 'c3000_pharmacology_toxicology_and_pharmaceutics',
 'c3100_physics_and_astronomy',
 'c3200_psychology',
 'c3300_social_sciences',
 'c3400_veterinary',
 'c3500_dentistry',
 'c3600_health_professions']

scopus_columns_names_2016 = [
 'sourcerecord_id',
 'title',
 'print_issn',
 'e_issn',
 'active_or_inactive',
 'coverage',
 'article_language_source_iso_codes',
 'citescore_2014',
 'sjr_2014',
 'snip_2014',
 'citescore_2015',
 'sjr_2015',
 'snip_2015',
 'citescore_2016', # new indicators to 2016
 'sjr_2016',
 'snip_2016',
 'medline_sourced_title',
 'open_acces_status',
 'articles_in_press_included',
 'added_to_list_since_october_2016',
 'source_type',
 'title_history_indication',
 'related_title_to_title_history_indication',
 'other_related_title_1',
 'other_related_title_2',
 'other_related_title_3',
 'publishers_name',
 'publisher_imprints_grouped_to_main_publisher',
 'publishers_country',
 'all_science_classification_codes_asjc',
 'top_level_life_sciences',
 'top_level_social_sciences',
 'top_level_physical_sciences',
 'top_level_health_sciences',
 'c1000_general',
 'c1100_agricultural_and_biological_sciences',
 'c1200_arts_and_humanities',
 'c1300_biochemistry_genetics_and_molecular_biology',
 'c1400_business_management_and_accounting',
 'c1500_chemical_engineering',
 'c1600_chemistry',
 'c1700_computer_science',
 'c1800_decision_sciences',
 'c1900_earth_and_planetary_sciences',
 'c2000_economics_econometrics_and_finance',
 'c2100_energy',
 'c2200_engineering',
 'c2300_environmental_science',
 'c2400_immunology_and_microbiology',
 'c2500_materials_science',
 'c2600_mathematics',
 'c2700_medicine',
 'c2800_neuroscience',
 'c2900_nursing',
 'c3000_pharmacology_toxicology_and_pharmaceutics',
 'c3100_physics_and_astronomy',
 'c3200_psychology',
 'c3300_social_sciences',
 'c3400_veterinary',
 'c3500_dentistry',
 'c3600_health_professions']


scopuscitscore_columns_names = [
 'scopus_sourceid',
 'title',
 'citescore',
 'percentile',
 'citation_count',
 'scholarly_output',
 'percent_cited',
 'snip',
 'sjr',
 'rank',
 'rank_out_of',
 'publisher',
 'type',
 'openaccess',
 'scopus_asjc_code_(sub-subject_area)',
 'scopus_sub-subject_area',
 'quartile',
 'top_10_(citescore_percentile)',
 'url',
 'print_issn',
 'eissn']


# WOS
wos_columns_names = [
 'rank',
 'title',
 'jcr_abbreviated_title',
 'issn',
 'total_cites',
 'journal_impact_factor',
 'impact_factor_without_journal_self_cites',
 'five_year_impact_factor',
 'immediacy_index',
 'citable_items',
 'cited_half_life',
 'citing_half_life',
 'eigenfactor_score',
 'article_influence_score',
 'percentage_articles_in_citable_items',
 'empty',
 'average_journal_impact_factor_percentile',
 'normalized_eigenfactor']

# CWTS
cwts_columns_names = [
 'title',
 'source_type',
 'print_issn',
 'electronic_issn',
 'asjc_field_ids',
 'year',
 'citing_source',
 'p',
 'ipp',
 'ipp_lower_bound',
 'ipp_upper_bound',
 'snip',
 'snip_lower_bound',
 'snip_upper_bound',
 'percentage_self_cit']

# DOAJ
doaj_columns_names = [
 'colecao',
 'title',
 'issn',
 'link_doaj',
 'ultimo_ano_no_doaj',
 'licenca_no_doaj',
 'licenca_scielo',
 'disponivel_doaj',
 'atualizado_no_doaj',
 'data_de_conferencia',
 'plataforma',
 'selo_doaj',
 'ti_envia_dados',
 'enviado_formulario_pelo_editor',
 'data_de_confirmacao_de_envio',
 'observacoes']
