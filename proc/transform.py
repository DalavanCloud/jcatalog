# coding: utf-8
'''
This script transform various data type in datetime format type to load in MongoDB.
'''
import os 
import sys
import datetime


PROJECT_PATH = os.path.abspath(os.path.dirname(''))
sys.path.append(PROJECT_PATH)


class Dates(object):

    def datatype(self, data):
        t = type(data)
        return t


    def data2string(self, data):
        if type(data) != str:
            s = str(data)
            return s
        else:
            return data


    def data2datetime(self, data):
        
        dt = self.datatype(data)

        if dt == int and len(str(data)) == 4:
            ds = self.data2string(data)
            sd = datetime.datetime.strptime(ds, '%Y')
            return sd

        if dt == str and len(data) == 7:
            sd = datetime.datetime.strptime(data, '%Y-%m')
            return sd

        if dt == str and len(data) == 10:
            sd = datetime.datetime.strptime(data, '%Y-%m-%d')
            return sd
        
        if dt == datetime.datetime:
            return data
