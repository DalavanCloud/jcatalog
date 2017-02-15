# coding: utf-8

from mongoengine import *


connect('journals-catalog')


class Scielo(DynamicDocument):
	is_scielo = IntField(required=True)
	issns = ListField()


class Scimago(DynamicDocument):
	is_scimago = IntField(required=True)


class Scopus(DynamicDocument):
	is_scopus = IntField(required=True)


class Scopus_Discontinued(DynamicDocument):
    pass


class Wos(DynamicDocument):
    pass    