# -*- coding: utf-8 -*-
'''
    @File        test  dblib MongoConnector
    @Author
    @Created On 2018-04-11
    @Updated On 2018-04-11
'''
import os
import sys
import time
from bson.objectid import ObjectId
pwd = os.path.dirname(os.path.realpath(__file__))
pwd2 = sys.path[0]
pardir = os.path.abspath(os.path.join(pwd, os.pardir))
sys.path.append(pardir)
from dblib.MongoConnector import MongoConnector

reload(sys)
sys.setdefaultencoding('utf8')


class MongoTest(object):
    def __init__():


def insertOne_test(conn, collection):
    try:
        for i in range(1, 10):
            value = {
                    # "_id" : ObjectId("5a571f6551d80beafd2fa33d"),
                    "name": 'aa_'+str(i),
                    "num": i,
                    "update":int(time.time())}
            conn.insert(collection, value)

        print("insertOne_test end!")
        return True
    except Exception as e:
        print(e)
        return False

def insertMany_test(conn, collection):
    try:
        values = []
        for i in range(10, 20):
            value = {
                    # "_id" : ObjectId("5a571f6551d80beafd2fa33d"),
                    "name": 'bb_'+str(i),
                    "num": i,
                    "updateTime":int(time.time())}
            values.append(value)
        conn.insert_many(collection, values)

        print("insertMany_test end!")
        return True
    except Exception as e:
        print(e)
        return False


def find_test(conn, collection):
    try:
        results = conn.find(collection)
        for item in results:
            print("num:", item.get('num'))

        print("find_test end!")
        return True
    except Exception as e:
        print(e)
        return False

def _findOne_test(conn, collection):
    try:
        query = {'num':5}
        result = conn.find_one(collection, query)
        return result
    except Exception as e:
        print(e)
        return None



def update_test(conn, collection):
    try:
        # update num=5
        query = {'num':5}
        value = {'$set':{'name':"aa_update",'updateTime':int(time.time())}}
        conn.update(collection, query, value)

        updated = _findOne_test(conn, collection)
        if not updated:
            print("find find update item info!!")

        print("Update Info: ")
        print("name      : ", updated.get('name'))
        print("updateTime: ", updated.get('updateTime'))
        return True
    except Exception as e:
        print(e)
        return False



def main():
    xmlpath = '../conf/SysSet.xml'
    myTable = "TestTable"

    start_time = time.time()
    myConn = MongoConnector(xmlpath)

    myConn.drop(myTable)

    ret = insertOne_test(myConn, myTable)
    if not ret:
        print("insertOne_test error!!!")
    ret = insertMany_test(myConn, myTable)
    if not ret:
        print("insertOne_test error!!!")

    end_time = time.time()
    print("Insert  time: %d" % (end_time-start_time))


    ret = find_test(myConn, myTable)
    if not ret:
        print("find_test error!!!")

    ret = update_test(myConn, myTable)
    if not ret:
        print("update_test error!!!")

    mycount = myConn.count(myTable, {'name': "aa_1"})
    print("count: ", mycount)



if __name__ == "__main__":
    main()