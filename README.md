# SyncNoteTools

## 说明
该工具是一个将`印象笔记`，`Evernote`等同步到`语雀`的工具。

后续将添加 `OneNote`，`有道云笔记`等同步到`语雀`中。


## 使用方案
配置文件为json格式，存储在当前目录下名为`cfg.json`的文件中
```json
{
  "evernoteHost": "app.yinxiang.com",
  "evernoteToken": "",
  "syncNoteDbPath": "SyncNoteDB.sqlite3",
  
  "yuqueToken": "",
  
  "qiniuAccess_key":"",
  "qiniuSecret_key":"",
  "qiniuBucket_name":"",
  "qiniuBucket_name":"",
  "syncEvernoteBookMap": [
    {
      "evernote":"enboo1",
      "yuque":"yqbook1"
    },
    {
      "evernote":"enbook2",
      "yuque":"yqbook1"
    }
  ]
}
```


## 版本
ver: 0.01
1. 通过印象笔记的API，监控印象笔记的变化。
2. 下载指定的笔记本的笔记原文，并保存为enml，html，md格式，其中enml中的图片附件，上传到七牛云存储中了。
3. 将下载到本地的笔记，上传到语雀的指定文件夹中。


## 鸣谢
1. enml转换为html的工具采用的是通过[ENMLToHTML](https://github.com/CarlLee/ENML_PY)进行改造。
1. html转markdown的工具采用的是通过[Tomd](https://github.com/gaojiuli/tomd)进行改造。


## TODO
- [ ] 一个配置界面 配置token，配置笔记本同步状态，获取笔记本同步状态
- [ ] Evernote，语雀，七牛的token校验，以及异常提示
- [ ] 将同步的处理，写入一个线程中，并与UI线程分离，方便UI线程监控
- [ ] 命令行启动增加参数的处理，包括配置文件位置，DB位置，是否启动GUI等
- [ ] 网络异常导致的上传图片失败的处理
- [ ] Evernote访问频率过快的异常处理
- [ ] 印象笔记markdown的处理，
- [ ] 印象笔记mindmap的处理
- [ ] 印象笔记修改笔记本后的重传机制，包括从A笔记本中删除，从B笔记本中添加。
- [ ] 对于印象笔记中 附件的处理
- [ ] 图片上传到不同的图床
- [ ] 对于OneNote，有道云笔记等笔记本的支持
