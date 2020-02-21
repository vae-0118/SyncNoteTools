# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py.py    
@Contact :   149759490@qq.com
@License :   MIT
@description :

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
20/2/18 22:42   vae        1.0         None
'''


import logging
import base64


import SyncNoteTyping as SNTypes

from requests import session
from typing import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import and_, or_, update, delete, insert

from sqlalchemy.ext.declarative import declarative_base

# 初始化数据库连接:
engine = create_engine('sqlite:///SyncNoteDB1.sqlite3'
                       #, echo=True
                       )

# 创建对象的基类:
Base = declarative_base()