# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py.py    
@Contact :   149759490@qq.com
@License :   MIT
@description :

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
20/2/20 4:50   vae        1.0         None
'''

import os
import qiniu.config

from qiniu import Auth, put_file, etag

from SyncNoteTyping import SystemConfig

class QiniuApi(object):
    #base_url = 'http://qiniuimg.vaeliu.com//fea78d35cfd45786932b44c5541416f0.gif'
    def __init__(self):
        sysCfg = SystemConfig()
        sysCfg.LoadConfigFile('cfg.json')

        self.access_key = sysCfg.QiniuAccess_key
        self.secret_key = sysCfg.QiniuSecret_key
        self.bucket_name = sysCfg.QiniuBucket_name
        self.base_url = sysCfg.QiniuBaseUrl


    def UploadPic(self, localfile) -> str :

        # 构建鉴权对象
        q = Auth(self.access_key, self.secret_key)
        # 要上传的空间
        self.bucket_name = 'vae-qiniu'

        filePath, fileName = os.path.split(localfile)
        # 上传后保存的文件名
        key = fileName
        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(self.bucket_name, key, 3600)
        # 要上传文件的本地路径
        #localfile = localfile
        ret, info = put_file(token, key, localfile)
        print(info)
        assert ret['key'] == key
        assert ret['hash'] == etag(localfile)
