# coding: utf-8

import unittest
import pyexcel


'''
Loading SciELO CSV file data
'''
SCIELO_JOURNALS = 'fixtures/scielo_journals.csv'

class ScieloLoadProcTest(unittest.TestCase):

    def setUp(self):

        scielo_sheet = pyexcel.get_sheet(file_name=SCIELO_JOURNALS, name_columns_by_row=0)

        scielo_sheet.column.format('extraction date', str)

        self.scielo_json = scielo_sheet.to_records()


    def test_scieloproc_study_unit(self):

        result = self.scielo_json[0]['study unit']

        expected = 'journal'
        
        self.assertEqual(expected, result)


    def test_scieloproc_type_objstudy_unit(self):

        result = type(self.scielo_json[0]['extraction date'])
        
        expected = str
        
        self.assertEqual(expected, result)


'''
Loading Scimago excel file data
'''
SCIMAGO_JOURNALS = 'fixtures/scimago_journals.xlsx'

class ScimagoLoadProcTest(unittest.TestCase):

    def setUp(self):

        scimago_sheet = pyexcel.get_sheet(file_name=SCIMAGO_JOURNALS, name_columns_by_row=0)

        self.scimago_json = scimago_sheet.to_records()

    def test_scimagoproc_print_issn(self):

        result = self.scimago_json[0]['Type']

        expected = 'journal'
        
        self.assertEqual(expected, result)


'''
Loading Scopus excel file data
'''
SCOPUS_JOURNALS = 'fixtures/scopus_journals.xlsx'

class ScopusLoadProcTest(unittest.TestCase):

    def setUp(self):

        scopus_sheet = pyexcel.get_sheet(file_name=SCOPUS_JOURNALS, name_columns_by_row=0)

        scopus_sheet.column.format('Print-ISSN', str)
        
        scopus_sheet.column.format('E-ISSN', str)

        self.scopus_json = scopus_sheet.to_records()

    def test_scopusproc_print_issn(self):

        result = self.scopus_json[0]['Print-ISSN']

        expected = '15343219'
        
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
