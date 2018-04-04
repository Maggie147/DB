# -*- coding: utf-8 -*-
'''
    @File        test  dblib MysqlConnector
    @Author
    @Created On 2018-04-04
    @Updated On 2018-04-04
'''
import os
import sys
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
# print(parentUrl)
sys.path.append(parentUrl)


from dblib.MysqlConnector import MysqlConnector
import time

reload(sys)
sys.setdefaultencoding('utf8')



def main():
    xmlpath = '../conf/SysSet.xml'
    testTable = "TestTable"

    start_time = time.time()

    mysql = MysqlConnector(xmlpath)

    # # create table
    ret = mysql.create_test(testTable)
    if not ret:
        print("create table [%s] failed!!!" % testTable)
    print("create table [%s] succeed!!!" % testTable)

    # insert info
    for i in range(0, 10):
        insertInfo = {'Name':'aa_'+str(i), 'Num':i, 'Content': 'aabbccdd_'+str(i)*6, 'Time':int(time.time())}
        mysql.insert_test(testTable, insertInfo)
    for i in range(11, 20):
        insertInfo = {'Name':'bb_'+str(i), 'Num':i, 'Content': 'aabbccdd_'+str(i)*6, 'Time':int(time.time())}
        mysql.insert_test(testTable, insertInfo)

    end_time = time.time()
    print("Insert  time: %d" % (end_time-start_time))

    # find_one
    queryInfo = {'filed':'Num', 'value': '5'}
    result = mysql.find_one_test(testTable, queryInfo)
    print(result)

    # find_many
    # queryInfo = {'filed':'Name', 'value': 'bb'}
    queryInfo = {'filed':'Num', 'value': '5'}
    result2 = mysql.find_many_test(testTable, queryInfo, limit=10)
    for item in result2:
        print(item)

    print("\n")
    result2 = mysql.find_test(testTable, 3)
    for item in result2:
        print(item)

    lastNum = mysql.get_last_Num_test(testTable)
    print("The last Num: %s"% str(lastNum))



if __name__ == "__main__":
    main()