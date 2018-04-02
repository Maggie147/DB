#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
    @File        ESConnector.py
    @Author
    @CreatedDate 2018-04-02
'''

from elasticsearch import Elasticsearch, ElasticsearchException
from xml.etree import ElementTree
import traceback
import urllib3

conffile = '../conf/SysSet.xml'

class ESConnector(object):
    def __init__(self, conffile=conffile):
        self.__client = None
        host = readConfig(conffile)
        connectES(host)


    def readConfig(self, xmlpath):
        try:
            tree = ET.ElementTree(file=xmlpath)
            # tree = ET.parse(xmlpath)
            root = tree.getroot()
            database = root.find('database')
            host_node= database.findall('node')
            host = []
            for node in host_node:
                try:
                    es_ip  = host_node.find('ip').text
                    es_port = host_node.find('es').text
                    host.append({'host': es_ip, 'port': int(es_port)})
                except Exception as e:
                    print("no a node named es or ip, Please Check config!!!")
                    pass
        except Exception as e:
            print("Read DataBase Config failed!!! \n error: %s \n" % e)
            sys.exit(1)
        return host

    def connectES(self, host):
        try:
            self.__client = Elasticsearch(host, timeout = 60)
        except Exception, e:
            print traceback.print_exc()
            sys.exit(1)

    def find(self, index, type, dsl, source = False):
        page = {}
        try:
            name = type
            if isinstance(type, list) is False:
                name = (type is not None and type.lower() or None)
            page = self.__client.search(index, name, dsl, _source = source)
        except Exception, e:
            print traceback.print_exc()
        finally:
            return page

    def count(self, index, type_name, dsl = '{}'):
        page = {}
        try:
            page = self.__client.count(index, type_name, dsl)
        except Exception, e:
            print traceback.print_exc()
        finally:
            return page

    def init_scroll(self, index, type, dsl):
        sid = ''; size = 0
        try:
            name = (type is not None and type.lower() or None)
            #page = self.__client.search(index, name, dsl, search_type = 'scan')
            page = self.__client.search(index, name, dsl, search_type = 'scan', scroll = '1m')
            sid = page['_scroll_id']
            size = page['hits']['total']
        except Exception, e:
            print traceback.print_exc()
        finally:
            return sid, size

    def scroll(self, sid):
        page = {}
        try:
            page = self.__client.scroll(scroll_id = sid, scroll = '1m')
        except Exception, e:
            print traceback.print_exc()
        finally:
            return page

    def bulk(self, index, doc_type, body):
        page = {'errors': True}
        try:
            page = self.__client.bulk(index = index.lower(), doc_type = doc_type.lower(), body = body)
        except Exception, e:
            if e.info.args[1][0] == 104:
                try:
                    i = 0
                    print 'rebulking.....'
                    while True:
                        docs = body[i:i+1000]
                        if not docs:
                            break
                        i += 1000

                        page = self.__client.bulk(index = index.lower(), doc_type = doc_type.lower(), body = docs)
                    print 'rebulk over.....'
                except Exception, e:
                    print traceback.print_exc()
            else:
                print traceback.print_exc()
        finally:
            return page

    def delete(self, index, doc_type, id):
        try:
            page = self.__client.delete(index = index.lower(), doc_type= doc_type.lower(), id = id)
        except Exception, e:
            print traceback.print_exc()
        finally:
            return page

    def delete_by_query(self, index, doc_type, body):
        try:
            sid, size = self.init_scroll(index, doc_type, body)
            while size > 0:
                page = self.scroll(sid)
                sid = page['_scroll_id']
                size = len(page['hits']['hits'])
                docs = []
                for doc in page['hits']['hits']:
                    docs.append({'delete': {'_id': doc['_id']}})
                if docs:
                    self.bulk(index, doc_type, docs)
        except Exception, e:
            print traceback.print_exc()

    def insert(self, index, doc_type, id, body):
        page = {}
        try:
            page = self.__client.index(index = index.lower(), doc_type= doc_type.lower(), id = id, body = body)
        except Exception, e:
            print traceback.print_exc()
        finally:
            return page