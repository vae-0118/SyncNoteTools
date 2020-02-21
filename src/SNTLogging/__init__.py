# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py.py    
@Contact :   149759490@qq.com
@License :   MIT

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
20/2/17 14:18   vae        1.0         None
'''
import logging

from SNTLogging import SNTLogging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s-%(levelname)s %(module)s:%(funcName)s %(lineno)d: %(message)s ')

logger = SNTLogging.logging.getLogger()
handler = SNTLogging.LoggerHandlerToDB()
logger.addHandler(handler)
