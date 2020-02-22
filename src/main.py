# -*- coding:utf-8 -*-

import logging
import SNTLogging

from SyncNoteTyping import *

from Controller import Controller


if __name__ == '__main__':
    # 显示版本号
    logging.info("SyncNoteTools " + "ver:" + PROGRAM_VERSION)

    # # 启动控制器
    sysCtrl = Controller()

    # 系统自检
    sysCtrl.CheckSys()

    # 主循环
    sysCtrl.DoLoop()

    pass