# -*- coding: utf-8 -*-
'''
    @File        MongoConnector.py
    @Author
    @CreatedDate 2018-04-02
'''

# from xml.etree import ElementTree
import xml.etree.ElementTree as ET
import pymongo, traceback
import time
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

conffile = '../conf/SysSet.xml'

class MongoConnector(object):
    def __init__(self, conffile=conffile):
        self.__client = None
        self.__db = None
        dbInfo = self.readConfig(conffile)
        self.connectMongoDB(dbInfo)

    def readConfig(self, xmlpath):
        DB = {}
        try:
            tree = ET.ElementTree(file=xmlpath)
            # tree = ET.parse(xmlpath)
            root = tree.getroot()
            database = root.find('database')
            DB['db_host']  = database.find('db_address').text
            DB['db_port'] = database.find('db_port').text
            DB['db_name'] = database.find('db_name').text
            DB['db_user'] = database.find('db_user').text
            DB['db_pwd']  = database.find('db_pwd').text
            DB['db_charset'] = 'utf8'
        except Exception as e:
            print("Read DataBase Config failed!!! \n error: %s \n" % e)
            sys.exit(1)
        return DB

    def connectMongoDB(self, DB={}):
        uri = 'mongodb://%s:%s@%s:%s/%s' % (DB['db_user'], DB['db_pwd'], DB['db_host'], DB['db_port'], DB['db_name'])
        try:
            self.__client = pymongo.MongoClient(host = uri, maxPoolSize = 1, socketKeepAlive = True)
            self.__db = self.__client[DB['db_name']]
        except Exception, e:
            print(traceback.print_exc())
            sys.exit(1)

    def __del__(self):
        if self.__client is not None:
            self.__client.close()
            self.__client = None

    def find_one(self, collection_name,  info):
        cursor = {}
        try:
            collection = self.__db[collection_name]
            cursor = collection.find_one(info)
        except pymongo.errors.PyMongoError, e:
            print(e)
        finally:
            #print '>>>>>>',type(cursor)
            return cursor

    def find(self, collection_name, query = None, field = None, sort = None, limit = 0):
        cursor = {}
        try:
            collection = self.__db[collection_name]
            cursor = collection.find(query, field, sort = sort, limit = limit)
        except Exception, e:
            print(traceback.print_exc())
        finally:
            return cursor

    def insert(self, collection_name, doc):
        try:
            collection = self.__db[collection_name]
            collection.insert_one(doc)
        except Exception, e:
            print(traceback.print_exc())

    def insert_many(self, collection_name, docs):
        results = None
        try:
            collection = self.__db[collection_name]
            results = collection.insert_many(docs, False)
        except Exception, e:
            print(traceback.print_exc())
        finally:
            return results

    def update(self, collection_name, query, field, upsert = False):
        try:
            collection = self.__db[collection_name]
            collection.update_one(query, field, upsert)
        except Exception, e:
            print(traceback.print_exc())

    def count(self, collection_name, query):
        c = 0
        try:
            collection = self.__db[collection_name]
            c = collection.count(query)
        except Exception, e:
            print(traceback.print_exc())
        finally:
            return c

    def aggregate(self, collection_name, pipeline):
        cursor = {}
        try:
            collection = self.__db[collection_name]
            cursor = collection.aggregate(pipeline)
        except Exception, e:
            print(traceback.print_exc())
        finally:
            return cursor

    def delete(self, collection_name, query = {}):
        try:
            collection = self.__db[collection_name]
            collection.delete_many(query)
        except Exception, e:
            print(traceback.print_exc())

    def save(self, collection_name, doc):
        try:
            collection = self.__db[collection_name]
            collection.save(doc)
        except Exception, e:
            print(traceback.print_exc())

    def drop(self, collection_name):
        try:
            collection = self.__db[collection_name]
            collection.drop()
        except pymongo.errors.PyMongoError,e:
            print(e)
