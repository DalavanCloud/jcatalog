# coding: utf-8

from mongoengine import *
import datetime


connect('journals-catalog')


class Scielo(DynamicDocument):
    creation_date = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()
    extraction_date = DateTimeField()
    issn_list = ListField()
    date_of_the_first_document = DateTimeField()
    date_of_the_last_document = DateTimeField()
    scholarone = IntField(required=True, min_value=0, default=0)
    ojs_scielo = IntField(required=True, min_value=0, default=0)
    is_scielo = IntField(required=True, min_value=1, default=1)
    is_scimago = IntField(required=True, min_value=0, default=0)
    is_scopus = IntField(required=True, min_value=0, default=0)
    is_wos = IntField(required=True, min_value=0, default=0)
    is_doaj = IntField(required=True, min_value=0, default=0)
    is_capes = IntField(required=True, min_value=0, default=0)
    #Indexes
    meta = {
        'indexes': [
            'issn_list',
            'title_country'
        ]
    }


class Scimago(DynamicDocument):
    creation_date = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()
    issn_list = ListField()
    is_scielo = IntField(required=True, min_value=0, default=0)
    is_scimago = IntField(required=True, min_value=1, default=1)
    is_scopus = IntField(required=True, min_value=0, default=0)
    is_wos = IntField(required=True, min_value=0, default=0)
    #Indexes
    meta = {
        'indexes': [
            'issn_list',
            'title_country'
        ]
    }


class Scopus(DynamicDocument):
    creation_date = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()
    issn_list = ListField()
    is_scielo = IntField(required=True, min_value=0, default=0)
    is_scimago = IntField(required=True, min_value=0, default=0)
    is_scopus = IntField(required=True, min_value=1, default=1)
    is_wos = IntField(required=True, min_value=0, default=0)
    #Indexes
    meta = {
        'indexes': [
            'issn_list',
            'title_country'
        ]
    }


class Wos(DynamicDocument):
    creation_date = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()
    issn_list = ListField()
    is_scielo = IntField(required=True, min_value=0, default=0)
    is_scimago = IntField(required=True, min_value=0, default=0)
    is_scopus = IntField(required=True, min_value=0, default=0)
    is_wos = IntField(required=True, min_value=1, default=1)
    #Indexes
    meta = {
        'indexes': [
            'issn_list',
            'title_country'
        ]
    }


class Cwts(DynamicDocument):
    creation_date = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()
    is_cwts = IntField(required=True, min_value=1, default=1)
    is_scielo = IntField(required=True, min_value=0, default=0)
    is_scimago = IntField(required=True, min_value=0, default=0)
    is_wos = IntField(required=True, min_value=0, default=0)
    issn_list = ListField()
    title_scielo = StringField()
    country_scielo = StringField()
    collection_scielo = StringField()
    status_current_scielo = StringField()
    title_scimago = StringField()
    coutry_scimago = StringField()
    #Indexes
    meta = {
        'indexes': [
            'issn_list',
            'title_country'
        ]
    }


class Submissions(DynamicDocument):
    creation_date = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()
    issn_list = ListField()
    scholarone = IntField(required=True, min_value=0, default=0)
    ojs_scielo = IntField(required=True, min_value=0, default=0)
    ojs_outro = IntField(required=True, min_value=0, default=0)
    outro = IntField(required=True, min_value=0, default=0)


class Doaj(DynamicDocument):
    creation_date = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()
    issn_list = ListField()


class Doajapi(DynamicDocument):
    creation_date = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()
    issn_list = ListField()
    

class Capes(DynamicDocument):
    creation_date = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()
    issn_list = ListField()


class Noscielo(DynamicDocument):
    creation_date = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()
    issn_list = ListField()


class Scimagoall(DynamicDocument):
    creation_date = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()
    issn_list = ListField()
    is_scielo = IntField(required=True, min_value=0, default=0)
    is_scimago = IntField(required=True, min_value=1, default=1)
    is_scopus = IntField(required=True, min_value=0, default=0)
    is_wos = IntField(required=True, min_value=0, default=0)
    #Indexes
    meta = {
        'indexes': [
            'issn_list',
            'title_country'
        ]
    }


class Scopuscitescore(DynamicDocument):
    creation_date = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()
    issn_list = ListField()
    #Indexes
    meta = {
        'indexes': [
            'issn_list',
            'title_country'
        ]
    }
