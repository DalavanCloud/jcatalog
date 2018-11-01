# wos_ciitations_report
import models

import xlsxwriter


def wos_citations():

    filename = 'wos_citations_report.xlsx'
    sheetname = 'scielo_wos_citations'
    workbook = xlsxwriter.Workbook('output/' + filename)
    worksheet = workbook.add_worksheet(sheetname)
    worksheet.freeze_panes(1, 0)
    # worksheet.set_row(0, 70)

    format_date_iso = workbook.add_format({'num_format': 'yyyy-mm-dd'})

    row = 0
    col = 0
    for h in ['extraction date',
              'title at WoS',
              'issn SciELO',
              'title at SciELO',
              'publisher name',
              'thematic areas',
              'is agricultural sciences',
              'is applied social sciences',
              'is biological sciences',
              'is engineering',
              'is exact and earth sciences',
              'is health sciences',
              'is human sciences',
              'is linguistics letters and arts',
              'is multidisciplinary',
              'collection',
              'WOS ALL',
              'WOS1 (SCIE-SSCI-AHCI)',
              'WOS2 (ESCI)',
              'query',
              'first year of pub',
              'last year of pub',
              'citations after the last year of pub (last year of pub + 1)',
              'citations in 2013',
              'citations in 2014',
              'citations in 2015',
              'citations in 2016',
              'citations in 2017',
              'citations in 2018',
              'citations in 2019',
              'total docs',
              'total docs first year of pub',
              'total docs last year of pub',
              'h-index',
              'h-index - average citations per item'
              ]:
        worksheet.write(row, col, h)
        col += 1

    citations = models.WosCitations.objects.filter(
        is_scielo=1).order_by('title').batch_size(5)
    # citations = models.WosCitations.objects.filter(
    # title='CUADERNOS DEL CENTRO DE ESTUDIOS EN DISENO Y COMUNICACION
    # ENSAYOS')

    row = 1

    for cit in citations:
        print(cit['title'])

        col = 0

        worksheet.write(row, col, cit['creation_date'], format_date_iso)
        col += 1

        worksheet.write(row, col, cit['title'])
        col += 1

        doc = models.Scielo.objects.filter(issn_scielo=cit['issn_scielo'])[0]

        if doc:
            # ISSN SciELO
            worksheet.write(row, col, doc.issn_scielo)
            col += 1

            worksheet.write(row, col, doc.title)
            col += 1

            # Publisher Name
            worksheet.write(row, col, doc.publisher_name)
            col += 1

            # Thematic Areas
            col = 5
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

            # collection
            worksheet.write(row, col, doc.collection)
            col += 1

            # is WoS ALL
            worksheet.write(row, col, doc.is_wos)
            col += 1

            # Wos ('SSCI-SSCI-AHCI')
            if doc.is_wos == 1:
                docwos = models.Wos.objects(id=str(doc.wos_id))[0]
                if any(i in docwos.indexes for i in ['scie', 'ssci', 'ahci']):
                    worksheet.write(row, col, 1)
                else:
                    worksheet.write(row, col, 0)
            else:
                worksheet.write(row, col, 0)
            col += 1

            # Wos ('ESCI')
            if doc.is_wos == 1:
                docwos = models.Wos.objects(id=str(doc.wos_id))[0]
                if 'esci' in docwos.indexes:
                    worksheet.write(row, col, 1)
                else:
                    worksheet.write(row, col, 0)
            else:
                worksheet.write(row, col, 0)
            col += 1

        col = 19
        # query and years
        worksheet.write(row, col, cit['query'])
        col += 1
        worksheet.write(row, col, cit['first_year'])
        col += 1
        worksheet.write(row, col, cit['last_year'])
        col += 1

        # citations after the last year
        nexty = str(cit['last_year'] + 1)
        if 'citations' in cit:
            next_year = cit['citations'][nexty]
            worksheet.write(row, col, next_year)
        col += 1

        # citations:
        for y in range(2013, 2020):
            if str(y) in cit['citations']:
                worksheet.write(row, col, cit['citations'][str(y)])
            col += 1

        # total docs
        worksheet.write(row, col, cit['total'])
        col += 1

        # total docs by year
        fy = str(cit['first_year'])
        ly = str(cit['last_year'])

        if fy in cit['total_year']:
            worksheet.write(row, col, cit['total_year'][fy])
        col += 1

        if ly in cit['total_year']:
            worksheet.write(row, col, cit['total_year'][ly])
        col += 1

        # h-index
        worksheet.write(row, col, cit['h_index'])
        col += 1
        worksheet.write(row, col, cit['h_index_avg_cit_item'])
        col += 1

        # avanca linha
        row += 1


def main():
    wos_citations()


if __name__ == "__main__":
    main()
