# -*- encoding: utf-8 -*-
"""
@File    :   DBOperator.py
@Contact :   149759490@qq.com
@License :   MIT
@description :

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
20/2/19 1:23   vae        1.0         None
"""

import logging
import base64

import evernote.edam.type.ttypes as Types

import DatabaseOperator.EvernoteDBOTyping as ENDBTypes
import DatabaseOperator.YuqueDBOTyping as YQDBTypes
import DatabaseOperator.DBOTyping as DBOTyping
import SyncNoteTyping as SNTypes

from requests import session
from typing import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import and_, or_, update, delete, insert

from YuqueAPI.simple_pyyuque_typing import *
from DatabaseOperator import *


class DBOperator(object):

    # 构建表
    ENDBTypes.Base.metadata.create_all(engine)

    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)

    def UpdateEvernotebooks(self, enNotebookList: Sequence[Types.Notebook]):
        '''
            更新印象笔记的 笔记本
        '''
        # 创建session对象:
        session = self.DBSession()

        # 清空表
        session.query(ENDBTypes.Notebook).delete()

        for enNotebook in enNotebookList:
            dbNotebook = ENDBTypes.Notebook(
                guid=enNotebook.guid,
                name=enNotebook.name,
                updateSequenceNum=enNotebook.updateSequenceNum,
                defaultNotebook=enNotebook.defaultNotebook,
                serviceCreated=enNotebook.serviceCreated,
                serviceUpdated=enNotebook.serviceUpdated,
                published=enNotebook.published,
                stack=enNotebook.stack,
            )
            session.add(dbNotebook)

        # 提交修改
        session.commit()

        # 关闭数据库
        session.close()

    def InsertEvernoteData(self, noteList: Sequence[Types.Note]):
        if noteList is None:
            return

        session = self.DBSession()

        for note in noteList:
            # 如果是有效数据 才记录到数据库中，不然就删除
            dbNote = ENDBTypes.Note(
                guid=note.guid,
                title=note.title,
                content=note.content,
                # contentHash=note.contentHash,
                contentLength=note.contentLength,
                created=note.created,
                updated=note.updated,
                deleted=note.deleted,
                active=note.active,
                updateSequenceNum=note.updateSequenceNum,
                notebookGuid=note.notebookGuid,
                # tagGuids=note.tagGuids,
                # resources=note.resources,
                # attributes=note.attributes,
                # tagNames=note.tagNames,
                syncToYuque=False,
                downloaded=False
            )
            # 删除原有的
            session.query(ENDBTypes.Note).filter(ENDBTypes.Note.guid == note.guid).delete()

            # 添加新数据
            session.add(dbNote)

            # 更新USN
            session.query(ENDBTypes.SyncState).delete()
            syncState = ENDBTypes.SyncState(
                updateCount=note.updateSequenceNum
            )
            session.add(syncState)

        # 提交修改
        session.commit()
        session.close()

    def GetEvernoteLocalUSN(self):
        '''
            获取本地的最后一次同步数值
        '''
        session = self.DBSession()
        state = session.query(ENDBTypes.SyncState).first()
        if state is None:
            # 第一次查询 是找不到合适的笔记本的
            return 0

        logging.debug(state.updateCount)

        updateCount = state.updateCount
        # session.commit()
        session.close()

        return updateCount

    def SaveEvernoteLocalUSN(self, localUSN: int):
        session = self.DBSession()
        # 更新USN
        session.query(ENDBTypes.SyncState).delete()
        syncState = ENDBTypes.SyncState(
            updateCount=localUSN
        )
        session.add(syncState)

        # 提交修改
        session.commit()
        session.close()

    def GetEvernoteFirstUnDonloadNoteInfo(self):
        '''
            获取未下载的数据
        '''
        session = self.DBSession()

        # 查找需要上传的笔记本
        res = session.query(DBOTyping.YuqueEvernoteBookMap).all()
        if res is None:
            session.close()
            return None

        uploadBookList = []
        for r in res:
            uploadBookList.append(r.evernoteNoteBookGuid)

        res = session.query(ENDBTypes.Note).filter(
            and_(ENDBTypes.Note.downloaded == False,
                 ENDBTypes.Note.active == True,
                 ENDBTypes.Note.notebookGuid.in_(uploadBookList))
        ).order_by(ENDBTypes.Note.updateSequenceNum.desc()).first()

        if res is None:
            session.close()
            return None
        else:
            guid = res.guid
            session.close()
            return guid

    def GetEvernoteFirstUnUploadNoteInfo(self) -> YQDBTypes.UnUploadNoteInfo:
        '''
            获取未上传的笔记信息
        '''
        session = self.DBSession()
        results: dict = {}

        # 找到印象笔记中所有待上传的笔记本
        res = session.query(DBOTyping.YuqueEvernoteBookMap).all()
        if res is None:
            session.close()
            return None

        uploadBookList = []
        for r in res:
            uploadBookList.append(r.evernoteNoteBookGuid)

        logging.debug(uploadBookList)

        # 找到第一条已经下载的笔记
        res = session.query(ENDBTypes.Note) \
            .filter(
            and_(ENDBTypes.Note.syncToYuque == False,
                 ENDBTypes.Note.notebookGuid.in_(uploadBookList),
                 ENDBTypes.Note.downloaded == True,
                 ENDBTypes.Note.active == True)
        ).order_by(ENDBTypes.Note.updateSequenceNum.desc()).first()

        if res is None:
            session.close()
            return None

        notebookGuid = res.notebookGuid
        noteGuid = res.guid
        title = res.title
        enml = res.enml
        html = res.html
        markdown = res.markdown

        # 找到语雀的笔记本
        res = session.query(DBOTyping.YuqueEvernoteBookMap).filter(
            DBOTyping.YuqueEvernoteBookMap.evernoteNoteBookGuid == notebookGuid).first()
        yuqueBookNamespace = res.yuqueBookNamespace

        noteInfo = YQDBTypes.UnUploadNoteInfo(
            notebookGuid=notebookGuid,
            noteGuid=noteGuid,
            title=title,
            yuqueBookNamespace=yuqueBookNamespace,
            enml=enml,
            html=html,
            markdown=markdown,
        )

        session.close()
        return noteInfo

    def SetEvernoteDownloadState(self, noteGuid: str, state: bool):
        '''
            标记文件的下载状态
        '''
        session = self.DBSession()
        session.query(ENDBTypes.Note).filter(ENDBTypes.Note.guid == noteGuid).update({"downloaded": state})
        session.commit()
        session.close()

        return

    def SetEvernoteUploadState(self, noteGuid: str, state: bool):
        '''
            标记文件的上传状态
        '''
        session = self.DBSession()
        session.query(ENDBTypes.Note).filter(ENDBTypes.Note.guid == noteGuid).update({"syncToYuque": state})
        session.commit()
        session.close()

        return

    def SaveEvernoteContent(self, noteGuid: str, enml: str, html: str, markdown: str):
        '''
            标记文件已经上传
        '''
        session = self.DBSession()
        session.query(ENDBTypes.Note) \
            .filter(ENDBTypes.Note.guid == noteGuid) \
            .update({"enml": enml,
                     'html': html,
                     'markdown': markdown})
        session.commit()
        session.close()

        return

    def UpdateYuqueBooks(self, booklist: Sequence[BookSerializer]):
        '''
            更新印象笔记的 笔记本
        '''
        # 创建session对象:
        session = self.DBSession()

        # 清空表
        session.query(YQDBTypes.YuqueBook).delete()

        for book in booklist:
            dbNotebook = YQDBTypes.YuqueBook(
                id=book.id,
                type=book.type,
                slug=book.slug,
                name=book.name,
                namespace=book.namespace,
                user_id=book.user_id,
                description=book.description,
                creator_id=book.creator_id,
                public=book.public,
                likes_count=book.likes_count,
                watches_count=book.watches_count,
                created_at=book.created_at,
                updated_at=book.updated_at,
            )
            session.add(dbNotebook)

        # 提交修改
        session.commit()

        # 关闭数据库
        session.close()

        return

    def UpdateYuqueEvernoteBookMap(self,
                                   bookmapList: Sequence[SNTypes.SystemConfig.SyncBookMap]):
        # 创建session对象:
        session = self.DBSession()

        # 清空原有的对应关系
        session.query(DBOTyping.YuqueEvernoteBookMap).delete()

        for bookmap in bookmapList:
            res = session.query(ENDBTypes.Notebook) \
                .filter(ENDBTypes.Notebook.name == bookmap.evernoteBook).first()
            evernoteNoteBookGuid = res.guid
            res = session.query(YQDBTypes.YuqueBook) \
                .filter(YQDBTypes.YuqueBook.name == bookmap.yuqueBook).first()
            yuqueBookNamespace = res.namespace

            dbmap = DBOTyping.YuqueEvernoteBookMap(
                evernoteNoteBookGuid=evernoteNoteBookGuid,
                yuqueBookNamespace=yuqueBookNamespace,
            )
            session.add(dbmap)

        # 提交修改
        session.commit()

        # 关闭数据库
        session.close()
