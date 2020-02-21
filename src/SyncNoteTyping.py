# -*- encoding: utf-8 -*-
'''
@File    :   SyncNoteTyping.py    
@Contact :   149759490@qq.com
@License :   MIT

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
20/2/17 13:27     vae        1.0         None
'''

import json
import logging
from builtins import set

from typing import Optional, Union, List
from enum import Enum

import os

# 应用程序的版本号
PROGRAM_VERSION = '0.0.1'

# 当前的路径
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

# 配置文件路径
CONFIG_FILE_NAME = 'cfg.json'
CONFIG_FILE_PATH = os.path.join(PROJECT_PATH, CONFIG_FILE_NAME)

# 默认的数据库的存储位置
SYNC_NOTE_DB_FILE_NAME = 'SyncNoteDB.sqlite3'

# 默认的数据库的存储位置
EVERNOTE_HOST = 'app.yinxiang.com'

# 印象笔记默认的下载位置
EVERNOTE_DOWNLOAD_PATH = os.path.join(PROJECT_PATH, 'Local', 'Evernote')


class SystemConfig(object):
    '''
        系统配置的参数
    '''

    def __init__(self, options: dict = None):
        if options is None:
            return
        self._yuqueToken = options.get("yuqueToken", "")
        self._evernoteToken = options.get("evernoteToken", "")
        self._evernoteHost = options.get("evernoteHost", EVERNOTE_HOST)
        self._qiniuAccess_key = options.get("qiniuAccess_key", "")
        self._qiniuSecret_key = options.get("qiniuSecret_key", "")
        self._qiniuBucket_name = options.get("qiniuBucket_name", "")
        self._qiniuBaseUrl = options.get("qiniuBaseUrl", "")

        self._bookMapList = options.get("syncEvernoteBookMap", [])
        # for bookmap in self._bookMapList:
        #     print(bookmap)
        #     print(bookmap['evernote'], bookmap['yuque'])

        self._syncNoteDbPath = options.get("syncNoteDbPath", SYNC_NOTE_DB_FILE_NAME)
        self._syncNoteDbPath = os.path.join(PROJECT_PATH, self._syncNoteDbPath)

    def LoadConfigFile(self, fileName: str = 'cfg.json'):
        with open(fileName, 'r', encoding='UTF-8') as f:
            cfg = f.read()
            logging.debug("配置文件\n" + cfg)
            cfg = json.loads(cfg)

            self.__init__(cfg)

    @property
    def YuqueToken(self) -> str:
        return self._yuqueToken

    @property
    def EvernoteToken(self) -> str:
        return self._evernoteToken

    @property
    def EvernoteHost(self) -> str:
        return self._evernoteHost

    @property
    def QiniuAccess_key(self) -> str:
        return self._qiniuAccess_key

    @property
    def QiniuSecret_key(self) -> str:
        return self._qiniuSecret_key

    @property
    def QiniuBucket_name(self) -> str:
        return self._qiniuBucket_name

    @property
    def QiniuBaseUrl(self) -> str:
        return self._qiniuBaseUrl

    @property
    def SyncNoteDbPath(self) -> str:
        return self._syncNoteDbPath

    class SyncBookMap(object):
        evernoteBook = ''
        yuqueBook = ''

    @property
    def BookMapList(self) -> list:
        bookmaplist = []
        for item in self._bookMapList:
            tmp = self.SyncBookMap()
            tmp.evernoteBook = item['evernote']
            tmp.yuqueBook = item['yuque']
            bookmaplist.append(tmp)

        return bookmaplist

    @property
    def SysConfig(self) -> dict:
        '''
            类 转换为 dict
        '''
        cfgDict = {
            "yuqueToken": self._yuqueToken,
            "evernoteToken": self._evernoteToken,
            "evernoteHost": self._evernoteHost,

            "qiniuAccess_key": self._qiniuAccess_key,
            "qiniuSecret_key": self._qiniuSecret_key,
            "qiniuBucket_name": self._qiniuBucket_name,
            "_qiniuBaseUrl": self._qiniuBaseUrl,

            "syncNoteDbPath": self._syncNoteDbPath,
        }

        return cfgDict
