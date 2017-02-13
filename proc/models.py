# coding: utf-8

from mongoengine import *


connect('journals-catalog')


class Scielo(DynamicDocument):
    pass


class Scimago(DynamicDocument):
	pass


class Wos(DynamicDocument):
	pass


class Scopus(DynamicDocument):
	pass


class Scopus_Discontinued(DynamicDocument):
	pass