# -*- encoding: utf-8 -*-
'''
@File    :   Controller.py    
@Contact :   149759490@qq.com
@License :   MIT
@description :

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
20/2/18 16:01   vae        1.0         None
'''

import os
import json
import logging

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.NoteStore as NoteStore

import EvernoteAPI.EnmlTools as Enml
import EvernoteAPI.tomd as tomd
import QiniuApi

import SyncNoteTyping

from evernote.api.client import EvernoteClient, Store

from DatabaseOperator.DBOperator import DBOperator as ENDBOperator


class Controller(object):
    _token = ""
    _client: EvernoteClient = None

    _db = ENDBOperator()

    def __init__(self, token: str, serviceHost: str):
        self._token = token
        self._client = self._GetNoteClient(token, serviceHost)
        if self._client is None:
            raise ValueError

    def _LoadLocalSyncState(self):
        '''
            加载本地已经同步的状态
        '''

        pass

    def SyncNoteTOC(self, maxNoteCnt: int = 10000):
        '''
            同步笔记的目录
        '''
        self._LoadLocalSyncState()

        self._SyncNotebookTOC()

        self._SyncNoteTOC(maxNoteCnt)

    def DownloadNote(self, noteGUID: str = None):
        '''
            下载笔记
        '''
        # 下载笔记
        # 查找未下载的笔记
        noteGuid = self._db.GetEvernoteFirstUnDonloadNoteInfo()

        if noteGuid is None:
            logging.debug("没有需要下载的文件了")
            return False

        # 下载笔记文件和资源
        noteStore = self._client.get_note_store()
        note = noteStore.getNote(self._client.token, noteGuid, True, True, True, True)
        logging.debug("download:" + noteGuid + ' ' + note.title)

        # 保存文件
        self._SaveNote(note)

        # 标记已经下载完成
        self._db.SetEvernoteDownloadState(note.guid, True)

        return True

    def _NoteToMD(self):
        '''
            将笔记变成MarkDown
        '''
        pass

    def _SyncNotebookTOC(self):
        '''
            同步目录结构
        '''
        # 获取类笔记本库
        noteStore = self._client.get_note_store()

        # 获取笔记本列表
        noteBookList = noteStore.listNotebooks()
        for notebook in noteBookList:
            logging.info("notebook:"+notebook.guid + "  " + notebook.name)

        # 写入数据库
        db = ENDBOperator()
        db.UpdateEvernotebooks(noteBookList)

        pass

    def _SyncNoteTOC(self, maxEntries: int):
        '''
            同步笔记的目录结构
        '''

        db = ENDBOperator()

        # 获取最后一次更新的内容
        self._client = EvernoteClient(token = self._token, service_host = 'app.yinxiang.com')
        noteStore = self._client.get_note_store()


        state = noteStore.getSyncState(self._client.token)
        updateCount = state.updateCount

        # 如果和数据库中的一致，就不需要更新了
        localUSN = db.GetEvernoteLocalUSN()

        logging.info("Evernote USN:%d, local USN:%d",
                     updateCount,
                     localUSN)
        if updateCount > localUSN:
            # 更新100条信息
            logging.info("需要更新数据啦")
            self._SyncNoteInfo(noteStore, localUSN, maxEntries)
        else:
            logging.info("暂时不用更新数据")

        pass

    def _SyncNoteInfo(self, noteStore: NoteStore.Client, localUSN: int, maxEntries: int):
        '''
            获取最新的笔记信息，并存储到数据库中
        '''
        f = NoteStore.SyncChunkFilter()
        f.includeNotes = True
        chunk = noteStore.getFilteredSyncChunk(self._client.token, localUSN, maxEntries, f)
        logging.debug(chunk)

        db = ENDBOperator()

        if chunk.notes is None:
            db.SaveEvernoteLocalUSN(chunk.updateCount)
        else:
            db.InsertEvernoteData(chunk.notes)

        pass

    def _GetNoteClient(self, token, serviceHost) -> EvernoteClient:
        '''
            Evernote操作的客户端
        '''
        client: EvernoteClient = EvernoteClient(token=token, service_host=serviceHost)

        user_store = client.get_user_store()

        # 检查版本
        version_ok = user_store.checkVersion(
            "Evernote EDAMTest (Python)",
            UserStoreConstants.EDAM_VERSION_MAJOR,
            UserStoreConstants.EDAM_VERSION_MINOR
        )

        version_ok = True
        if version_ok is False:
            logging.debug("SDK版本校验错误")
            client = None
        else:
            logging.debug("SDK版本校验正确")

        return client

    def _SaveNote(self, note: Types.Note):
        '''
            下载文件到指定的目录
        '''
        folder = os.path.join(SyncNoteTyping.EVERNOTE_DOWNLOAD_PATH, note.notebookGuid, note.guid)
        if not os.path.exists(folder):
            os.makedirs(folder)

        qiniu = QiniuApi.QiniuApi()
        res_folder = os.path.join(folder, 'resources')
        if note.resources is not None:
            for res in note.resources:
                url = Enml.DownloadResource(res, res_folder)
                if url is not None:
                    # TODO 上传失败后的处理
                    # ToDo 上传的数据 存储到数据库中
                    qiniu.UploadPic(url)

        fileName = os.path.join(folder, note.guid)
        html = Enml.ENMLToHTML(note.content, True, True, qiniu.base_url)

        with open(fileName + '.enml', 'w', encoding='UTF-8') as f:
            f.write(note.content)

        html = str(html, encoding="utf-8")
        with open(fileName + '.html', 'w', encoding='UTF-8') as f:
            f.write(html)

        mdTxt = tomd.Tomd(html).markdown
        with open(fileName + '.md', 'w', encoding='UTF-8') as f:
            f.write(mdTxt)

        self._db.SaveEvernoteContent(note.guid, note.content, html, mdTxt)

        return
