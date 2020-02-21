# -*- encoding: utf-8 -*-
'''
@File    :   EvernoteDBOTyping.py
@Contact :   149759490@qq.com
@License :   MIT
@description :

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
20/2/18 22:44   vae        1.0         None
'''

from sqlalchemy import Column, String, Integer, Boolean, BLOB, MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import evernote.edam.type.ttypes as Types

from DatabaseOperator import *

# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    name = Column(String(20))


class Notebook(Base):
    __tablename__ = 'Evernote_Notebook'

    # 表结构
    guid = Column(String(), primary_key=True)
    name = Column(String())
    updateSequenceNum = Column(String())
    defaultNotebook = Column(Boolean)
    serviceCreated = Column(Integer)
    serviceUpdated = Column(Integer)
    publishing = Column(String())
    published = Column(Boolean)
    stack = Column(String())
    sharedNotebookIds = Column(String())
    sharedNotebooks = Column(String())
    businessNotebook = Column(String())
    contact = Column(Integer)
    restrictions = Column(String())


class SyncState(Base):
    __tablename__ = 'Evernote_SyncState'

    updateCount = Column(Integer, primary_key=True)


class Note(Base):
    '''
        印象笔记的 单条笔记信息
    '''
    __tablename__ = 'Evernote_Note'

    guid = Column(String(), primary_key=True)
    title = Column(String())
    content = Column(String())
    contentHash = Column(String())
    contentLength = Column(Integer)
    created = Column(String())
    updated = Column(String())
    deleted = Column(String())
    active = Column(Boolean)
    updateSequenceNum = Column(Integer)
    notebookGuid = Column(String())
    tagGuids = Column(String())
    resources = Column(String())
    attributes = Column(String())
    tagNames = Column(String())
    syncToYuque = Column(Boolean, default=False)
    downloaded = Column(Boolean, default=False)
    enml = Column(String())
    html = Column(String())
    markdown = Column(String())


class Resource(Base):
    '''
        印象笔记的 单条笔记信息
    '''
    __tablename__ = 'Evernote_Resource'

    guid = Column(String, primary_key=True)
    noteGuid = Column(String)
    data = Column(BLOB)
    mime = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    duration = Column(Integer)
    active = Column(Boolean)
    recognition = Column(BLOB)
    attributes = Column(String)
    updateSequenceNum = Column(Integer)
    alternateData = Column(BLOB)


