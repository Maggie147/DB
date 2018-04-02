# -*- coding: utf-8 -*-
'''
    @File        MysqlConnector.py
    @Author
    @CreatedDate 2018-04-02
'''

# from xml.etree import ElementTree
import xml.etree.ElementTree as ET
import MySQLdb
import time
import os
reload(sys)
sys.setdefaultencoding('utf8')

conffile = '../conf/SysSet.xml'

class MysqlConnector(object):
    def __init__(self, conffile=conffile):
        self.conn = None
        self.cur = None
        dbInfo = readConfig(conffile)
        connectMysqlDB(dbInfo)

    def readConfig(self, xmlpath):
        DB = {}
        try:
            tree = ET.ElementTree(file=xmlpath)
            # tree = ET.parse(xmlpath)
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
            self.cur = conn.cursor()
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
            self.cur.close()
            self.conn.close()
        except Exception as e:
            print('exit error!!!')

    def create_test(self):
        sql = "CREAT TABLE 'TUser'(\
        'Id' int(11) unsigned NOT NULL AUTO_INCREMENT,\
        'Name' varchar(30) NOT NULL,\
        'Ip' char(15) NOT NULL,\
        'Num' int(10) UNSIGNED NOT NULL,\
        'Content' TEXT NULL,\
        'Time' DATETIME NOT NULL,\
        PRIMARY KEY (`Id`),\
        INDEX `TUser_Index_IP` (`IPaddress`),\
        )"
        try:
            self.cur.execute(sql)
        except Exception as e:
            conn.rollback()
            print(e)


    def insert_test(self, tablename, values):
        sql = "insert into %s(Id, Name, Ip, Num, Content, Time) values(null, '%s', '%s', '%d', '%s', '%d')" % (\
            tablename,\
            MySQLdb.escape_string(str(values[0]).strip()), \
            MySQLdb.escape_string(str(values[1]).strip()), \
            int(str(values[2]).strip()), \
            MySQLdb.escape_string(str(values[3]).strip()), \
            MySQLdb.FROM_UNIXTIME(values[5].strip()))
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception, e:
            conn.rollback()
            print(traceback.print_exc())
            print("Insert_test tablename[%s] failed!!!"%tablename)


    def find_test(self, tablename, startid, limit=10):
        values = None
        # queryVar = '%'+query+'%'
        # sql = "select * from %s where Domain like \'%s\';" % (tablename, queryVar)
        sql = "select Id, Name, INET_NTOA(Ip), Num, (FROM_UNIXTIME)Time, from %s where Id > %d order by Id limit %d;" % (\
            tablename, int(startid), self.limit)
        try:
            count = self.cursor.execute(sql)
            values = self.cursor.fetchall()
            if not values:
                print("not more data!!!")
        except Exception, e:
            conn.rollback()
            print(traceback.print_exc())
            print("find failed!!!")
        # begin_id += count
        return values


    def find_one_test(self, tablename, id):
        sql = "select * from %s where Id = %s" % (tablename, id)
        try:
            self.cursor.execute(sql)
            values = self.cursor.fetchone()
        except Exception as e:
            conn.rollback()
            print(e)
        return values

    def get_last_test(self, tablename):
        num = 0
        sql = "select Num from %s order by MailId desc limit 1"%tablename
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if result:
                num = result[0][0]
        except Exception as e:
            conn.rollback()
            print(e)
        return num