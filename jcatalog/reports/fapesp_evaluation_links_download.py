# coding: utf-8
import os
import sys
import datetime
import xlsxwriter

import models


PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)

today = datetime.datetime.now()

prelink = 'http://static.scielo.org/fapesp_evaluation/'


def main():
    scielo_fields = [
        'date',
        'ISSN SciELO',
        'Journal',
        'Publisher Name',
        'link to form to evaluation',
        'link to worksheet of the editor',
        'link page of journal',
        'thematic_areas',  # thematic areas scielo
        'agricultural sciences',
        'applied social sciences',
        'biological sciences',
        'engineering',
        'exact and earth sciences',
        'health sciences',
        'human sciences',
        'linguistics letters and arts',
        'multidisciplinary']

    workbook = xlsxwriter.Workbook('output/links_download.xlsx')
    worksheet = workbook.add_worksheet('Fapesp Avaliação SciELO')

    format_date = workbook.add_format({'num_format': 'yyyy-mm-dd'})

    # Header
    row = 0
    col = 0

    for h in scielo_fields:
        worksheet.write(0, col, h)
        col += 1

    row = 1

    # Somente periódicos que entraram antes de 2016
    query = models.Scielofapesp.objects.filter(
        fapesp_evaluation__2018__evaluated=1)
    print(query.count())
    # query = models.Scielo.objects.filter(issn_list='0101-4714')

    for doc in query:
        at = []

        if doc['title_is_multidisciplinary'] == 1:
            at.append("Multidisciplinary")
        else:
            ats = doc['title_thematic_areas'].replace(
                " ", "_").replace(",", "")
        at = [a for a in ats.split(';')]

        for a in at:

            col = 0

            issn = doc['issn_scielo']

            worksheet.write(row, col, today, format_date)
            col += 1
            worksheet.write(row, col, issn)
            col += 1
            worksheet.write(row, col, doc['title'])
            col += 1
            worksheet.write(row, col, doc['publisher_name'])
            col += 1

            form = prelink + 'Formulario-avaliacao-Fapesp-SciELO-' + \
                a + '-' + issn + '-20180723.docx'
            worksheet.write(row, col, form)
            col += 1

            file = prelink + 'Fapesp-avaliacao-SciELO-' + issn + '-20180713.xlsx'
            worksheet.write(row, col, file)
            col += 1

            if 'url' in doc['api']:
                worksheet.write(row, col, doc.api['url'])
            col += 1

            # Thematic Areas
            col = 7
            for k in [
                'title_thematic_areas',
                'title_is_agricultural_sciences',
                'title_is_applied_social_sciences',
                'title_is_biological_sciences',
                'title_is_engineering',
                'title_is_exact_and_earth_sciences',
                'title_is_health_sciences',
                'title_is_human_sciences',
                'title_is_linguistics_letters_and_arts',
                'title_is_multidisciplinary'
            ]:
                if k in doc:
                    worksheet.write(row, col, doc[k])
                col += 1

            row += 1


if __name__ == '__main__':
    main()
