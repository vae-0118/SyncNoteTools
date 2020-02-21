# -*- encoding: utf-8 -*-
'''
@File    :   SNTLogging.py    
@Contact :   149759490@qq.com
@License :   MIT

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
20/2/17 14:18   vae        1.0         None
'''

import logging
import pymysql
import time
import sqlite3
import os

LOG_DB_TYPE = 'SQLITE3'
#LOG_DB_TYPE = 'MySQL'


class LoggerHandlerToDB(logging.Handler):
    def __init__(self):
        """
            初始化日志模块
        """
        logging.Handler.__init__(self)

        if LOG_DB_TYPE == 'MySQL':
            self.MySQL_init()
        elif LOG_DB_TYPE == 'SQLITE3':
            self.sqlite_init()

    def emit(self, record):
        """
        写入日志的方法
        :param record:
        :return:
        """
        if LOG_DB_TYPE == 'MySQL':
            self.MySQL_emit(record)
        elif LOG_DB_TYPE == 'SQLITE3':
            self.sqlite_emit(record)

    def MySQL_init(self):
        self._connect = pymysql.Connect(
            **TMConfig.db_config
        )

        # 获取游标
        self._cursor = self._connect.cursor()

    def MySQL_emit(self, record):
        """
        用MySQL记录日志的方法
        :param record:

        :return:

        """
        format_string = "%Y-%m-%d %H:%M:%S"
        time_stamp = int(record.created)
        time_array = time.localtime(time_stamp)
        asctime = time.strftime(format_string, time_array)
        # 插入日志信息
        sql = '''
            INSERT INTO 
              tb_logging(asctime, levelname, filename, lineno, funcName, stack_info, message) 
            VALUES 
              ('%s', '%s', '%s', %d, '%s', '%s', '%s');
              '''
        msg = pymysql.escape_string(record.message)
        data = (asctime, record.levelname, record.filename, record.lineno,
                record.funcName, record.stack_info, msg)
        self._cursor.execute(sql % data)
        self._connect.commit()

    def sqlite_init(self):
        """
            sqlite3 日志表的记录方法
        :return:
        """
        # 获取游标
        self._connect = sqlite3.connect('log.db',
                                        check_same_thread=False)
        self._cursor = self._connect.cursor()
        create_tb_cmd = '''
                CREATE TABLE IF NOT EXISTS "tb_log"(
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "asctime" integer,
                "levelname" TEXT,
                "filename" TEXT,
                "lineno" INTEGER,
                "funcName" TEXT,
                "stack_info" TEXT,
                "message" TEXT
            );
                '''
        # 主要就是上面的语句
        self._connect.execute(create_tb_cmd)

    def sqlite_emit(self, record):
        """
        通过sqlite写入数据库的方法
        :param record:
        :return:
        """
        sql = '''
                 INSERT INTO 
                     tb_log(asctime, levelname, filename, lineno, funcName, stack_info, message) 
                 VALUES 
                     (:asctime, :levelname, :filename, :lineno, :funcName, :stack_info, :message);
                 '''
        data = {
            'asctime': int(record.created),
            'levelname': record.levelname,
            'filename': record.filename,
            'lineno': record.lineno,
            'funcName': record.funcName,
            'stack_info': record.stack_info,
            'message': record.message
        }
        self._cursor.execute(sql, data)
        self._connect.commit()
