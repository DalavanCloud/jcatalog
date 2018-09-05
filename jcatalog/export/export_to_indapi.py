import sys
import time
from datetime import datetime

from mongoengine import DynamicDocument, fields, connect

# import models from Journals-Catalog
import models


# Get the indapi database
indapi = connect('indapi', alias='indapi').get_database('indapi')

# Get the indapi collections
journal_api = indapi.get_collection('journal')
jcr_api = indapi.get_collection('jcr')
scopus_api = indapi.get_collection('scopus')
scimago_api = indapi.get_collection('scimago')
googlescholar_api = indapi.get_collection('googlescholar')


class Journal(DynamicDocument):
    # created_at = fields.DateTimeField(default=datetime.now)
    issn_scielo = fields.StringField(required=True)
    title = fields.StringField(required=True)
    meta = {
        'db_alias': 'indapi',
        'collection': 'journal',
        'indexes': [
            'issn_scielo',
            'title'
        ]}


class Indicators(DynamicDocument):
    journal_id = fields.ReferenceField(Journal)
    issn_scielo = fields.StringField()
    years = fields.ListField()
    indicators = fields.DictField()
    meta = {
        'db_alias': 'indapi',
        'abstract': True,
        'indexes': [
            'issn_scielo',
            'years'
        ]}


class Jcr_api(Indicators):
    meta = {'collection': 'jcr'}
    pass


class Scopus_api(Indicators):
    meta = {'collection': 'scopus'}
    pass


class Scimago_api(Indicators):
    meta = {'collection': 'scimago'}
    pass


class Google_api(Indicators):
    meta = {'collection': 'google'}
    pass

# drop
Journal.drop_collection()
Jcr_api.drop_collection()
Scopus_api.drop_collection()
Scimago_api.drop_collection()
Google_api.drop_collection()

time.sleep(3)

# Query in journals-catalog database - collection: Scielo
scielo = models.Scielo.objects().batch_size(5)

for qscielo in scielo:

    print(qscielo.issn_scielo)

    # instance class Journal
    journal = Journal()

    # inserir dados de journal
    journal.switch_db(db_alias='indapi')
    # journal.created_at = datetime.now()
    journal.title = qscielo.title
    journal.issn_scielo = qscielo.issn_scielo
    journal.collection = qscielo.collection
    journal.collections = qscielo.collections

    journal.save()

    # Insert sources to the list collections below
    sources = []

    mdata = journal.to_mongo()

    # Insert data in collection
    # i.e col = 'jcr'
    for col in ['google',
                'jcr',
                'scopus',
                'scimago'
                ]:

        if col == 'google':

            gind = Google_api()
            flag = 0

            for y in range(2012, datetime.now().year + 1):
                if any(k in qscielo for k in [
                        'google_scholar_h5_' + str(y),
                        'google_scholar_m5_' + str(y)]):
                    sources.append('google')
                    gind.journal_id = journal
                    gind.issn_scielo = qscielo.issn_scielo
                    flag = 1

                if 'google_scholar_h5_' + str(y) in qscielo:
                    gind.years.append(y)
                    gind.indicators[str(y)] = {'google_scholar_h5': qscielo[
                        'google_scholar_h5_' + str(y)]}

                if 'google_scholar_m5_' + str(y) in qscielo:
                    gind.years.append(y)
                    gind.indicators = gind.indicators
                    gind.indicators[str(y)]['google_scholar_m5'] = qscielo[
                        'google_scholar_m5_' + str(y)]

            if flag > 0:
                gind.years = list(set(gind.years))
                gind.years.sort()
                gind.save()

            sources = list(set(sources))
            mdata['sources'] = sources
            journal.modify(**mdata)

        else:
            # i.e models.Jcr
            dbcol = getattr(models, col.capitalize())
            # i.e. Jcr_api() - instances the class Jcr_api
            class_name = getattr(
                sys.modules[__name__], col.capitalize() + '_api')

            if getattr(qscielo, 'is_' + col) == 1:

                sources.append(col)

                if sources:
                    mdata = journal.to_mongo()
                    sources.sort()
                    sources = list(set(sources))
                    mdata['sources'] = sources

                    journal.modify(**mdata)

                # query to db collection with the indicator in jornals catalog
                # i.e.:
                # models.Scopus.objects.filter(id=str(qscielo.scopus.id))[0]
                q_ind = dbcol.objects.filter(
                    id=str(getattr(qscielo, col + '_id')))[0]

                # instance to class <col>
                # i.e. ind = Jcr()
                ind = class_name()

                ind.journal_id = journal
                ind.issn_scielo = qscielo.issn_scielo

                for k in q_ind.__dict__.keys():
                    for y in range(1998, datetime.now().year + 1):
                        if str(y) == k:
                            ind.years.append(y)
                            ind.years.sort()
                            ind.indicators[str(y)] = q_ind[str(y)]

                # save to indicator collection
                ind.save()
