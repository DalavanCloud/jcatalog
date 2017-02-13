# coding: utf-8

import unittest
import pyexcel


'''
Loading SciELO CSV file data
'''
scielosheet = pyexcel.get_sheet(file_name='fixtures/scielo_journals.csv', name_columns_by_row=0)
scielosheet.column.format('extraction date', str)
scielojson = scielosheet.to_records()

class ScieloLoadProcTest(unittest.TestCase):

    def test_scieloproc_study_unit(self):

        result = scielojson[0]['study unit']

        expected = 'journal'
        
        self.assertEqual(expected, result)


    def test_scieloproc_type_objstudy_unit(self):

        result = type(scielojson[0]['extraction date'])
        
        expected = str
        
        self.assertEqual(expected, result)


'''
Loading Scimago excel file data
'''
scimagosheet = pyexcel.get_sheet(file_name='fixtures/scimago_journals.xlsx', name_columns_by_row=0)
scimagojson = scimagosheet.to_records()

class ScimagoLoadProcTest(unittest.TestCase):

    def test_scimagoproc_print_issn(self):

        result = scimagojson[0]['Type']

        expected = 'journal'
        
        self.assertEqual(expected, result)


'''
Loading Scopus excel file data
'''
scopussheet = pyexcel.get_sheet(file_name='fixtures/scopus_journals.xlsx', name_columns_by_row=0)
scopussheet.column.format('Print-ISSN', str)
scopussheet.column.format('E-ISSN', str)
scopusjson = scopussheet.to_records()

class ScopusLoadProcTest(unittest.TestCase):

    def test_scopusproc_print_issn(self):

        result = scopusjson[0]['Print-ISSN']

        expected = '15343219'
        
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()