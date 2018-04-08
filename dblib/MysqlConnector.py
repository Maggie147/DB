# -*- coding: utf-8 -*-
'''
    @File        MysqlConnector.py
    @Author
    @Created On 2018-04-02
    @Updated On 2018-04-08
'''
import os
import sys
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)

# from xml.etree import ElementTree
import xml.etree.ElementTree as ET
import MySQLdb
import time
reload(sys)
sys.setdefaultencoding('utf8')


conffile = '../conf/SysSet.xml'
class MysqlConnector(object):
    def __init__(self, conffile=conffile):
        self.conn = None
        self.cursor = None
        dbInfo = self.readConfig(conffile)
        self.connectMysqlDB(dbInfo)

    def readConfig(self, xmlpath):
        DB = {}
        try:
            tree = ET.ElementTree(file=xmlpath)             # tree = ET.parse(xmlpath)
            root = tree.getroot()
            database = root.find('database')
            DB['db_host']  = database.find('db_address').text
            DB['db_name'] = database.find('db_name').text
            DB['db_user'] = database.find('db_user').text
            DB['db_pwd']  = database.find('db_pwd').text
            DB['db_charset'] = 'utf8'
        except Exception as e:
            print("Read DataBase Config failed!!! \n error: %s \n" % e)
            sys.exit(1)
        return DB

    def connectMysqlDB(self, DB={}):
        try:
            self.conn = MySQLdb.connect(host    = DB['db_host'],
                                        user    = DB['db_user'],
                                        passwd  = DB['db_pwd'],
                                        db      = DB['db_name'],
                                        charset = DB['db_charset'])
            self.cursor = self.conn.cursor()
            self.cursor.execute("SET NAMES utf8")
            if not self.conn:
                print("connect mysql failed!!!")
                sys.exit(1)
            print("connect mysql succeed...")
        except MySQLdb.Error, e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print('exit error!!!')


    def create_test(self, tablename='TestTable'):
        sql = '''CREATE TABLE IF NOT EXISTS `%s` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` char(50) DEFAULT NULL,
  `Num` int(11) DEFAULT NULL,
  `Content` TEXT NULL,
  `Time` DATETIME DEFAULT NULL,
  PRIMARY KEY (`Id`),
  INDEX `%s_Index_Num` (`Num`)
);''' % (tablename, tablename)
        try:
            self.cursor.execute(sql)
            return True
        except Exception as e:
            self.conn.rollback()
            print(e)
            print("sql: %s" % sql)
            return False


    def insert_test(self, tablename, values):
        sql = "insert into %s(Id, Name, Num, Content, Time) values(null, '%s', '%d', '%s', FROM_UNIXTIME('%s')  )" % (\
            tablename,\
            MySQLdb.escape_string(str(values['Name']).strip()), \
            values['Num'], \
            MySQLdb.escape_string(values['Content']).strip(), \
            str(values['Time']))

        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception, e:
            self.conn.rollback()
            print(traceback.print_exc())
            print("Insert_test tablename[%s] failed!!!"%tablename)


    def find_one_test(self, tablename, query):
        sql = "select * from {tablename} where {filed} = {value};".format(
            tablename = tablename,
            filed = query['filed'],
            value = query['value'])
        try:
            self.cursor.execute(sql)
            values = self.cursor.fetchone()
        except Exception as e:
            self.conn.rollback()
            print(e)
        return values


    def find_many_test(self, tablename, query=None, limit=10):
        values = []
        if query:
            queryValue = '%'+query['value']+'%'
            sql = "select * from %s where %s like \'%s\' order by Id limit %d;" % (tablename, query['filed'], queryValue, limit)
        else:
            sql = "select * from %s order by Id limit %d;" % (tablename, limit)

        try:
            self.cursor.execute(sql)
            values = self.cursor.fetchall()
        except Exception as e:
            self.conn.rollback()
            print(e)
            print("sql: %s" % sql)
        return values


    def find_test(self, tablename, startid, limit=10):
        values = []
        sql = "select Id, Name, Num, UNIX_TIMESTAMP(Time) from {tablename} where Id > {startid} order by Id limit 10;".format(
            tablename = tablename,
            startid = startid)                                                                        # (INET_NTOA)
        try:
            count = self.cursor.execute(sql)
            values = self.cursor.fetchall()
            # begin_id += count
        except Exception, e:
            self.conn.rollback()
            print(e)
            print("sql: %s" % sql)
        return values


    def get_last_Id_test(self, tablename):
        num = 0
        sql = "select Num from {} order by Id desc limit 1".format(tablename)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if result:
                num = result[0][0]
        except Exception as e:
            self.conn.rollback()
            print(e)
        return num


def test():
    mysql = MysqlConnector(conffile)            # conffile = '../conf/SysSet.xml'
    testTable = "TestTable"

    # create table
    ret = mysql.create_test(testTable)
    if not ret:
        print("create table [%s] failed!!!" % testTable)
    print("create table [%s] succeed!!!" % testTable)

    # insert info
    for i in range(0, 10):
        insertInfo = {'Name':'aa_'+str(i), 'Num':i, 'Content': 'aabbccdd_'+str(i)*6, 'Time':int(time.time())}
        mysql.insert_test(testTable, insertInfo)
    for i in range(10, 20):
        insertInfo = {'Name':'bb_'+str(i), 'Num':i, 'Content': 'aabbccdd_'+str(i)*6, 'Time':int(time.time())}
        mysql.insert_test(testTable, insertInfo)

    # find_one
    queryInfo = {'filed':'Num', 'value': '5'}
    result = mysql.find_one_test(testTable, queryInfo)
    print("find_one_test : ", result)

    # find_many
    queryInfo = {'filed':'Name', 'value': 'aa'}
    # queryInfo = {'filed':'Num', 'value': '5'}
    result2 = mysql.find_many_test(testTable, queryInfo, limit=10)
    for item in result2:
        print(item)

    print("\n")
    result2 = mysql.find_test(testTable, startid=3)
    for item in result2:
        print(item)

    lastNum = mysql.get_last_Id_test(testTable)
    print("The last Id: %s"% str(lastNum))



if __name__ == '__main__':
    test()