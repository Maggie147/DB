# -*- encoding: utf-8-*-
'''
    @File    test  dblib.MongoConnector
    @Author
    @Created On 2018-04-11
    @Updated On 2018-04-12
'''
# py3 = True if sys.version > '3' else False

import os
import sys
import time
from bson.objectid import ObjectId
pwd = os.path.dirname(os.path.realpath(__file__))       #pwd2 = sys.path[0]
pardir = os.path.abspath(os.path.join(pwd, os.pardir))
sys.path.append(pardir)
from dblib.MongoConnector import MongoConnector

reload(sys)
sys.setdefaultencoding('utf8')

g_iDEBUG = 0
def DEBUG(*value):
    if g_iDEBUG == 1:
        t = time.strftime("%Y-%m-%d %H:%M:%S")
        filename = sys.argv[0][sys.argv[0].rfind(os.sep)+1:]
        print "[python2.7][%s, %s]:" % (filename, t),
        for i in value:
            print i,
        print ""

class MongoTest(object):
    def __init__(self, xmlpath, tablename, debug=1):
        global g_iDEBUG
        g_iDEBUG = debug
        self.conn = MongoConnector(xmlpath)
        self.collection = tablename

        try:
            self.conn.drop(tablename)
        except Exception as e:
            pass

    def insertOne_test(self):
        try:
            for i in range(1, 10):
                value = {
                        # "_id" : ObjectId("5a571f6551d80beafd2fa33d"),
                        "name": 'aa_'+str(i),
                        "num": i,
                        "updateTime":int(time.time())}
                self.conn.insert(self.collection, value)

            DEBUG("insertOne_test end!")
        except Exception as e:
            DEBUG(e)
            DEBUG("insertOne_test failed!!!")

    def insertMany_test(self):
        try:
            values = []
            for i in range(10, 20):
                value = {
                        # "_id" : ObjectId("5a571f6551d80beafd2fa33d"),
                        "name": 'bb_'+str(i),
                        "num": i,
                        "updateTime":int(time.time())}
                values.append(value)
            self.conn.insert_many(self.collection, values)

            DEBUG("insertMany_test end!")
        except Exception as e:
            DEBUG(e)
            DEBUG("insertMany_test failed!!!")

    def find_test(self):
        try:
            DEBUG("find_test...")
            results = self.conn.find(self.collection, limit=9)
            for item in results:
                DEBUG("\t\tname: {}\t num: {}\t updateTime: {}".format(item.get('name'), item.get('num'), item.get('updateTime')) )
            DEBUG("find_test end!")
        except Exception as e:
            DEBUG(e)
            DEBUG("find_test failed!!!")

    def update_test(self):
        try:
            DEBUG("update_test...")
            query = {'num':5}
            value = {'$set':{'name':"aa_update",'updateTime':int(time.time())}}
            self.conn.update(self.collection, query, value)

            value = self._findOne_test(query)
            if not value:
                DEBUG("Not find update info!!")
            else:
                DEBUG("\t\tUpdated Info:")
                DEBUG("\t\tname: {}\t num:{}\t updateTime:{}".format(value.get('name'), value.get('num'), value.get('updateTime')) )

            DEBUG("update_test end!")
        except Exception as e:
            DEBUG(e)
            DEBUG("update_test failed!!!")

    def count_test(self):
        try:
            DEBUG("count_test...")
            query = {'name': "aa_1"}
            mycount = self.conn.count(self.collection, query)
            DEBUG("\t\t'{0}'' info count: {1}".format(self.collection, mycount))

            DEBUG("count_test end!")
        except Exception as e:
            DEBUG(e)
            DEBUG("count_test failed!!!")

    def _findOne_test(self, query):
        try:
            result = self.conn.find_one(self.collection, query)
            return result
        except Exception as e:
            DEBUG(e)
            return None


def main():
    start_time = time.time()

    xmlpath = '../conf/SysSet.xml'
    myTable = "TestTable"

    testObj = MongoTest(xmlpath, myTable)

    testObj.insertOne_test()

    testObj.insertMany_test()

    testObj.find_test()

    testObj.update_test()

    testObj.count_test()

    end_time = time.time()
    DEBUG("Test last time: ", (end_time-start_time))


if __name__ == "__main__":
    main()
