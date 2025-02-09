# coding: utf-8
'''
WOS Update
'''
import datetime
import logging
import pyexcel
import models
from accent_remover import *


logging.basicConfig(
    filename='logs/wos_loader.info.txt',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def wos_update():
    sheet = pyexcel.get_sheet(
        file_name='data/wos/2018 WOS CAT LIST.xlsx',
        sheet_name='import',
        name_columns_by_row=0)

    wos_json = sheet.to_records()

    for rec in wos_json:

        print(rec['title'])

        title_low = accent_remover(rec['title'].replace(
            " & ", " and ").replace("&", "and").lower())
        rec['title_lower'] = title_low
        rec['title_country'] = '%s-%s' % (title_low,
                                          rec['country'].lower())

        title_low_2mjl = accent_remover(rec['title'].lower())
        rec['title_low_2mjl'] = title_low_2mjl
        rec['title_country_2mjl'] = '%s-%s' % (title_low_2mjl,
                                               rec['country'].lower())

        query = models.Wos.objects.filter(title_low_2mjl=title_low_2mjl)

        if query:

            # Thematic Areas
            if 'category' in rec and 'thematic_areas' in query[0]:
                tarea = rec['category']
                if tarea not in query[0]['thematic_areas']:
                    tareas = list(query[0]['thematic_areas'])
                    tareas.append(tarea)
                    rec['thematic_areas'] = list(set(tareas))

                del rec['category']

            rec['updated_at'] = datetime.datetime.now()

            # update
            query[0].modify(**rec)

        else:
            # Thematic Areas
            if 'category' in rec:
                rec['thematic_areas'] = []
                rec['thematic_areas'].append(rec['category'])

            del rec['category']

            # save
            models.Wos(**rec).save()

    num_posts = models.Wos.objects().count()
    msg = u'Registred %d posts in Wos collection' % num_posts
    logger.info(msg)
    print(msg)


def wos_indexes():
    # Add indexes and ISSN List
    sheet = pyexcel.get_sheet(
        # file_name='data/wos/master_journal_list_181003_02_import.xlsx',
        file_name='data/wos/master_journal_list_181003_02_import.xlsx',
        sheet_name='import',
        name_columns_by_row=0)

    wos_json = sheet.to_records()

    for rec in wos_json:

        print(rec['journal'])

        title_low_2mjl = accent_remover(rec['journal'].lower())
        rec['title_low_2mjl'] = title_low_2mjl

        query = models.Wos.objects.filter(title_low_2mjl=title_low_2mjl)

        if query:
            if 'country' in rec and rec['country'] != 'BRAZIL':
                del rec['country']

            # title_low = accent_remover(rec['journal'].replace(
            #     " & ", " and ").replace("&", "and").lower())
            # rec['title_lower'] = title_low

            # if 'country' in rec:
            #     rec['title_country'] = '%s-%s' % (title_low,
            #                                       rec['country'].lower())
            # if 'country' in rec:
            #     rec['title_country_2mjl'] = '%s-%s' % (title_low_2mjl,
            #                                            rec['country'].lower())
            # ISSN LIST
            if 'issn' in rec:
                issn = rec['issn']
                if issn not in query[0]['issn_list']:
                    issn_list = list(query[0]['issn_list'])
                    issn_list.append(issn)
                    rec['issn_list'] = list(set(issn_list))

            # WOS INDEXES
            if 'indexes' in query[0]:
                index = rec['index']
                if index not in query[0]['indexes']:
                    index_list = list(query[0]['indexes'])
                    index_list.append(index)
                    rec['indexes'] = list(set(index_list))
            else:
                rec['indexes'] = []
                rec['indexes'].append(rec['index'])

            del rec['index']
            del rec['journal']

            rec['updated_at'] = datetime.datetime.now()

            # update
            query[0].modify(**rec)
        else:
            rec['title'] = rec['journal']

            title_low = accent_remover(rec['journal'].replace(
                " & ", " and ").replace("&", "and").lower())
            rec['title_lower'] = title_low

            if 'country' in rec and rec['country'] == 'BRAZIL':
                rec['title_country'] = '%s-%s' % (title_low,
                                                  rec['country'].lower())

            # ISSN LIST
            if 'issn' in rec:
                rec['issn_list'] = []
                rec['issn_list'].append(rec['issn'])

            # WOS INDEXES
            rec['indexes'] = []
            rec['indexes'].append(rec['index'])

            del rec['index']
            del rec['journal']

            # save
            models.Wos(**rec).save()


def main():
    # wos_update()
    wos_indexes()

if __name__ == "__main__":
    main()
