# coding: utf-8
'''
This script reads data from various sources to process and store in MongoDB.
'''
import pyexcel
import logging
import models
import datetime


logging.basicConfig(filename='logs/scielodatesnfo.txt', level=logging.INFO)
logger = logging.getLogger(__name__)


def scielodates():
    scielo_sheet = pyexcel.get_sheet(
        file_name='data/scielo/documents_dates_network.csv',
        name_columns_by_row=0)

    # Key correction
    cols = [
        'extraction_date',
        'study_unit',
        'collection',
        'issn_scielo',
        'issns',
        'title_at_scielo',
        'title_thematic_areas',
        'title_is_agricultural_sciences',
        'title_is_applied_social_sciences',
        'title_is_biological_sciences',
        'title_is_engineering',
        'title_is_exact_and_earth_sciences',
        'title_is_health_sciences',
        'title_is_human_sciences',
        'title_is_linguistics,_letters_and_arts',
        'title_is_multidisciplinary',
        'title_current_status',
        'pid',
        'document_publishing_year',
        'document_type',
        'document_is_citable',
        'document_submitted_at',
        'document_submitted_at_year',
        'document_submitted_at_month',
        'document_submitted_at_day',
        'document_accepted_at',
        'document_accepted_at_year',
        'document_accepted_at_month',
        'document_accepted_at_day',
        'document_reviewed_at',
        'document_reviewed_at_year',
        'document_reviewed_at_month',
        'document_reviewed_at_day',
        'document_published_as_ahead_of_print_at',
        'document_published_as_ahead_of_print_at_year',
        'document_published_as_ahead_of_print_at_month',
        'document_published_as_ahead_of_print_at_day',
        'document_published_at',
        'document_published_at_year',
        'document_published_at_month',
        'document_published_at_day',
        'document_published_in_scielo_at',
        'document_published_in_scielo_at_year',
        'document_published_in_scielo_at_month',
        'document_published_in_scielo_at_day',
        'document_updated_in_scielo_at',
        'document_updated_in_scielo_at_year',
        'document_updated_in_scielo_at_month',
        'document_updated_in_scielo_at_day']

    for i, k in enumerate(cols):
        scielo_sheet.colnames[i] = k

    scielo_json = scielo_sheet.to_records()

    models.Scielodates.drop_collection()

    for register in scielo_json:
        rec = dict(register)
        for key, value in rec.items():
            if type(value) == datetime.date:
                rec[key] = str(rec[key])

        # convert issn int type to str type
        if type(rec['issns']) != str:
            rec['issns'] = Issn().issn_hifen(rec['issns'])
            msg = u'issn converted: %s - %s' % (rec['issns'], rec['title'])
            logger.info(msg)

        # convert in list
        if type(rec['issns']) == str:
            rec['issns'] = rec['issns'].split(';')
            rec['issn_list'] = []
            rec['issn_list'].append(rec['issn_scielo'])
            for i in rec['issns']:
                if i not in rec['issn_scielo']:
                    rec['issn_list'].append(i)

        # remove empty keys
        rec = {k: v for k, v in rec.items() if v or v == 0}

        mdata = models.Scielodates(**rec)
        mdata.save()

    num_posts = models.Scielodates.objects().count()
    msg = u'Registred %d posts in SciELO Dates collection' % num_posts
    logger.info(msg)
    print(msg)


def main():
    # SciELO Network csv
    scielodates()


if __name__ == "__main__":
    main()
