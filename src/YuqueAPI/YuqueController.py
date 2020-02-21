# -*- encoding: utf-8 -*-
'''
@File    :   YuqueController.py    
@Contact :   149759490@qq.com
@License :   MIT
@description :

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
20/2/20 4:31   vae        1.0         None
'''

import logging
import SyncNoteTyping
import YuqueAPI.simple_pyyuque as YuqueClient

import DatabaseOperator.EvernoteDBOTyping as DBTypes

from YuqueAPI.simple_pyyuque_typing import *
from YuqueAPI.simple_pyyuque_utils import *

from DatabaseOperator.DBOperator import DBOperator


class DocData(object):
    notebook: str = ""
    id: int = 0
    title: str = ""
    slug: str = ""
    public: Union[DocPublic, int] = DocPublic.PRIVATE
    markdown: str = ""

    def __init__(self, **options):
        self.notebook = options.get('notebook', '')
        self.title = options.get('title', '')
        self.id = options.get('id', 0)
        self.slug = options.get('slug', '')
        self.public = options.get('public', DocPublic.PRIVATE)
        self.body = options.get('body', '')


class YuqueController(object):
    _client: YuqueClient = None

    _db = DBOperator()

    def __init__(self, token: str, appName: str = 'vae'):
        self._client = YuqueClient.SimplePyYuQueAPI(token, appName)

    def UploadDoc(self):
        '''
            上传文档到语雀
        '''
        doc = self._GetFirstUploadDoc()

        if doc is None:
            return False

        self._DoUploadDoc(doc)

        return True

    def _GetFirstUploadDoc(self) -> Optional[DocData]:
        '''
            获取第一个未上传的文件信息
        '''
        doc = DocData()

        uploadInfo = self._db.GetEvernoteFirstUnUploadNoteInfo()
        if uploadInfo is None:
            logging.debug("没有需要上传的文件了")
            return None

        doc.notebook = uploadInfo.yuqueBookNamespace
        doc.title = uploadInfo.title
        doc.slug = uploadInfo.noteGuid
        doc.public = DocPublic.PRIVATE
        doc.markdown = uploadInfo.markdown

        return doc

    def GetDoc(self, notebook, slug) -> Optional[DocDetailSerializer]:
        docClient = self._client.Doc()
        try:
            res = docClient.get_docs_detail(
                namespace=notebook,
                slug=slug)
        except Exception as e:
            logging.debug("配置文件错误:" + str(e))
            return None

        logging.debug(res)
        return res

    def UpdateDoc(self, doc: DocData):
        docClient = self._client.Doc()
        res = docClient.update_docs(
            namespace=doc.notebook,
            id=doc.id,
            slug=doc.slug,
            title=doc.title,
            body=doc.markdown)

        res = self.GetDoc(doc.notebook, doc.slug)
        if len(res.body) < 10:
            logging.debug(res.body)
            return None

        return res

    def CreateDoc(self, doc: DocData):
        docClient = self._client.Doc()
        res = docClient.create_docs(
            namespace=doc.notebook,
            slug=doc.slug,
            title=doc.title,
            body=doc.markdown)

        res = self.GetDoc(doc.notebook, doc.slug)
        if len(res.body) < 10:
            logging.debug(res.body)
            return None

        return res

    def SyncNoteTOC(self):
        """
            同步笔记本目录
        """
        userClient = self._client.User()
        userid = userClient.user.id

        repo = self._client.Repo()
        toc = repo.get_users_repos(id=userid).book_serializer_list
        logging.debug(toc)
        for menu in toc:
            logging.info("book:" + menu.name)

        self._db.UpdateYuqueBooks(toc)

    def _DoUploadDoc(self, doc: DocData):
        if len(doc.markdown) == 0:
            self._db.SetEvernoteUploadState(doc.slug, True)
            return

        # 原有文档是否存在
        netDoc = self.GetDoc(doc.notebook, doc.slug)
        if netDoc is None:
            # 如果不存在，用创建
            res = self.CreateDoc(doc)
        else:
            # 如果存在，用更新
            doc.id = netDoc.id
            res = self.UpdateDoc(doc)

        if res is not None:
            # 标记上传完成
            self._db.SetEvernoteUploadState(doc.slug, True)
            logging.info(doc.title + "上传到语雀成功")
        else:
            logging.debug("上传失败了哦")

        return
