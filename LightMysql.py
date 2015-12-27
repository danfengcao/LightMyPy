#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import time, re

class LightMysql:
    """Lightweight python class connects to MySQL. """

    _dbconfig = None
    _cursor = None
    _connect = None
    _error_code = '' # error_code from MySQLdb

    TIMEOUT_DEADLINE = 30 # quit connect if beyond 30S
    TIMEOUT_THREAD = 10 # threadhold of one connect
    TIMEOUT_TOTAL = 0 # total time the connects have waste

    def __init__(self, dbconfig):

        try:
            self._dbconfig = dbconfig
            self.dbconfig_test(dbconfig)
            self._connect = MySQLdb.connect(
                host=self._dbconfig['host'],
                port=self._dbconfig['port'],
                user=self._dbconfig['user'],
                passwd=self._dbconfig['passwd'],
                db=self._dbconfig['db'],
                charset=self._dbconfig['charset'],
                connect_timeout=self.TIMEOUT_THREAD)
        except MySQLdb.Error, e:
            self._error_code = e.args[0]
            error_msg = "%s --- %s" % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), type(e).__name__), e.args[0], e.args[1]
            print error_msg

            # reconnect if not reach TIMEOUT_DEADLINE.
            if self.TIMEOUT_TOTAL < self.TIMEOUT_DEADLINE:
                interval = 0
                self.TIMEOUT_TOTAL += (interval + self.TIMEOUT_THREAD)
                time.sleep(interval)
                return self.__init__(dbconfig)
            raise Exception(error_msg)

        self._cursor = self._connect.cursor(MySQLdb.cursors.DictCursor)

    def dbconfig_test(self, dbconfig):
        flag = True
        if type(dbconfig) is not dict:
            print 'dbconfig is not dict'
            flag = False
        else:
            for key in ['host','port','user','passwd','db']:
                if not dbconfig.has_key(key):
                    print "dbconfig error: do not have %s" % key
                    flag = False
            if not dbconfig.has_key('charset'):
                self._dbconfig['charset'] = 'utf8'

        if not flag:
            raise Exception('Dbconfig Error')
        return flag

    def query(self, sql, ret_type='all'):
        try:
            self._cursor.execute("SET NAMES utf8")
            self._cursor.execute(sql)
            if ret_type == 'all':
                return self.rows2array(self._cursor.fetchall())
            elif ret_type == 'one':
                return self._cursor.fetchone()
            elif ret_type == 'count':
                return self._cursor.rowcount
        except MySQLdb.Error, e:
            self._error_code = e.args[0]
            print "Mysql execute error:",e.args[0],e.args[1]
            return False

    def dml(self, sql):
        '''update or delete or insert'''
        try:
            self._cursor.execute("SET NAMES utf8")
            self._cursor.execute(sql)
            self._connect.commit()
            type = self.dml_type(sql)
            # if primary key is auto increase, return inserted ID.
            if type == 'insert':
                return self._connect.insert_id()
            else:
                return True
        except MySQLdb.Error, e:
            self._error_code = e.args[0]
            print "Mysql execute error:",e.args[0],e.args[1]
            return False

    def dml_type(self, sql):
        re_dml = re.compile('^(?P<dml>\w+)\s+', re.I)
        m = re_dml.match(sql)
        if m:
            if m.group("dml").lower() == 'delete':
                return 'delete'
            elif m.group("dml").lower() == 'update':
                return 'update'
            elif m.group("dml").lower() == 'insert':
                return 'insert'
        print "%s --- Warning: '%s' is not dml." % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), sql)
        return False


    def rows2array(self, data):
        '''transfer tuple to array.'''
        result = []
        for da in data:
            if type(da) is not dict:
                raise Exception('Format Error: data is not a dict.')
            result.append(da)
        return result

    def __del__(self):
        '''free source.'''
        try:
            self._cursor.close()
            self._connect.close()
        except:
            pass

    def close(self):
        self.__del__()
