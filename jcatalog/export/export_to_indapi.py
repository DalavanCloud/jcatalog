import sys
from datetime import datetime

from mongoengine import DynamicDocument, fields

# import models from Journals-Catalog
import models


# Get the indapi database
indapi = models.connect('indapi').get_database('indapi')

# Get the indapi collections
journal_api = indapi.get_collection('journal')
jcr_api = indapi.get_collection('jcr')
scopus_api = indapi.get_collection('scopus')
scimago_api = indapi.get_collection('scimago')
googlescholar_api = indapi.get_collection('googlescholar')


class Journal(DynamicDocument):
    created_at = fields.DateTimeField(default=datetime.now)
    issn_scielo = fields.StringField(required=True)
    title = fields.StringField(required=True)
    indicators = fields.ListField()
    meta = {
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
        'abstract': True,
        'indexes': [
            'issn_scielo',
            'years'
        ]}


class Jcr(Indicators):
    pass


class Scopus(Indicators):
    pass


class Scimago(Indicators):
    pass


class Googlescholar(Indicators):
    pass


# Query in journals-catalog database - collection: Scielo
list_issn = ["0074-0276", "0044-5967"]

for i in list_issn:
    qscielo = models.Scielo.objects.filter(issn_scielo=i)[0]

    print(qscielo.issn_scielo)

    # instance class Journal
    journal = Journal()

    # inserir dados de journal
    journal.created_at = datetime.now()
    journal.title = qscielo.title
    journal.issn_scielo = qscielo.issn_scielo
    journal.collection = qscielo.collection

    journal.save()
    # Insere na coleção
    if journal:
        journal_api.insert_one(journal.to_mongo())

    # Inserts indicators to the list collections below
    for col in ['jcr',
                'scopus',
                'scimago']:

        # i.e col = 'jcr'

        # i.e models.Jcr
        dbcol = getattr(models, col.capitalize())

        # i.e. Jcr() - instances the class Jcr
        class_name = getattr(sys.modules[__name__], col.capitalize())()

        if getattr(qscielo, 'is_' + col) == 1:
            indicators = journal.indicators
            indicators.append(col)
            # print(indicators)
            journal_api.update_one(
                {"_id": journal.id},
                {"$set": {"indicators": indicators}})

            # query to db collection with the indicator in jornals catalog
            q_ind = dbcol.objects.filter(
                id=str(
                    getattr(qscielo, col + '_id')
                )
            )[0]

            # instance to class <col>
            # i.e. ind = Jcr()
            ind = class_name

            ind.journal_id = journal
            ind.issn_scielo = qscielo.issn_scielo
            ind.indicators = {}

            for k in q_ind.__dict__.keys():
                for y in range(1999, datetime.now().year + 1):
                    if str(y) == k:
                        ind.years.append(y)
                        ind.years.sort()
                        ind.indicators[str(y)] = q_ind[str(y)]

            ind.save()

        # save to indicator collection
        # i.e. jcr_api.insert_one(jcr.to_mongo())
        if ind:
            getattr(sys.modules[__name__], col +
                    '_api').insert_one(ind.to_mongo())
