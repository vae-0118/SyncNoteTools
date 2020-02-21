# -*- encoding: utf-8 -*-
'''
@File    :   YuqueDBOTyping.py.py
@Contact :   149759490@qq.com
@License :   MIT
@description :

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
20/2/21 21:55   vae        1.0         None
'''

from sqlalchemy import Column, String, Integer, Boolean, BLOB, MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import evernote.edam.type.ttypes as Types

from DatabaseOperator import *

class YuqueBook(Base):
    __tablename__ = 'Yuque_Book'

    # 表结构
    id = Column(Integer, primary_key=True)
    type = Column(String())
    slug = Column(String())
    name = Column(String())
    namespace = Column(String())
    user_id = Column(Integer)
    description = Column(String())
    creator_id = Column(Integer)
    public = Column(Integer)
    likes_count = Column(Integer)
    watches_count = Column(Integer)
    created_at = Column(Integer)
    updated_at = Column(Integer)


class UnUploadNoteInfo(object):
    '''
        未上传的笔记信息
    '''
    __slots__ = ['notebookGuid',
                 'noteGuid',
                 'title',
                 'yuqueBookNamespace',
                 'enml',
                 'html',
                 'markdown']

    def __init__(self, **options):
        self.notebookGuid = options.get('notebookGuid')
        self.noteGuid = options.get('noteGuid')
        self.title = options.get('title')
        self.yuqueBookNamespace = options.get('yuqueBookNamespace')
        self.enml = options.get('enml')
        self.html = options.get('html')
        self.markdown = options.get('markdown')