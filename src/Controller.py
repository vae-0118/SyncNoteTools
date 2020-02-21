# -*- coding:utf-8 -*-

import os
import time

from EvernoteAPI.Controller import Controller as EvernoteCtrl
from YuqueAPI.YuqueController import YuqueController as YuqueCtrl
from SyncNoteTyping import SystemConfig

from DatabaseOperator.DBOperator import DBOperator

class Controller(object):
    '''
        系统控制器
    '''

    def __init__(self):

        sysCfg = SystemConfig()
        sysCfg.LoadConfigFile('cfg.json')

        # 获取配置
        self._configuration = sysCfg

        # 构造印象笔记的客户端
        self._evernoteCtrl = EvernoteCtrl(
            self._configuration.EvernoteToken,
            self._configuration.EvernoteHost)

        self._yuqueCtrl = YuqueCtrl(self._configuration.YuqueToken, 'vae')

    def CheckSys(self):
        '''
            系统校验
            包括 token 的校验
            数据库的校验
        '''

        pass

    def CheckToken(self):
        '''
            校验token
        '''
        pass

    def LoadLocalSyncState(self):
        '''
            加载本地的同步状态
        '''
        # 加载印象笔记同步状态
        self._evernoteCtrl.LoadLocalSyncState()

        pass

    def LoadSyncBookMap(self):
        '''
            加载同步状态
        '''
        pass

    def SyncNoteTOC(self):
        '''
            同步笔记
        '''
        # 同步印象笔记目录
        self._evernoteCtrl.SyncNoteTOC()

        # 同步语雀的笔记目录
        self._yuqueCtrl.SyncNoteTOC()

        # 同步映射关系
        self._UpdateSyncMap()

        pass

    def SyncNote(self, maxEntries: int = 100):
        '''
            同步笔记的内容
        '''
        for i in range(maxEntries):
            # 下载最新的一个待同步的印象笔记
            hasDownloader = False
            hasDownloader = self._evernoteCtrl.DownloadNote()

            # 上传到语雀中
            hasUpload = False
            hasUpload = self._yuqueCtrl.UploadDoc()

            if hasDownloader == False and hasUpload == False:
                return False

        return True

    def _UpdateSyncMap(self):
        db = DBOperator()
        db.UpdateYuqueEvernoteBookMap(self._configuration.BookMapList)

        return

    def DoLoop(self):
        '''
            同步笔记的主循环
        '''
        while True:
            # 同步笔记的目录
            self.SyncNoteTOC()

            # 同步笔记
            hasSync = self.SyncNote()
            if hasSync == False:
                time.sleep(60)
            else:
                time.sleep(10)

        return

