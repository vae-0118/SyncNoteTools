# -*- encoding: utf-8 -*-
'''
@File    :   DBOTyping.py    
@Contact :   149759490@qq.com
@License :   MIT
@description :

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
20/2/21 22:01   vae        1.0         None
'''


from sqlalchemy import Column, String, Integer, Boolean, BLOB, MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import evernote.edam.type.ttypes as Types

from DatabaseOperator import *

class YuqueEvernoteBookMap(Base):
    '''
        印象笔记的 单条笔记信息
    '''
    __tablename__ = 'Yuque_Evernote_Book_Map'

    evernoteNoteBookGuid = Column(String, primary_key=True)
    yuqueBookNamespace = Column(String)
