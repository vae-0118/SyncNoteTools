# -*- encoding: utf-8 -*-
'''
@File    :   EnmlTools.py    
@Contact :   149759490@qq.com
@License :   MIT
@description :

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
20/2/19 16:41   vae        1.0         None
'''

import os
import hashlib
import binascii

from bs4 import BeautifulSoup
from typing import Sequence

import evernote.edam.type.ttypes as Types

MIME_TO_EXTESION_MAPPING = {
    'image/png': '.png',
    'image/jpg': '.jpg',
    'image/jpeg': '.jpg',
    'image/gif': '.gif'
}

REPLACEMENTS = [
    ("&quot;", "\""),
    ("&amp;apos;", "'"),
    ("&apos;", "'"),
    ("&amp;", "&"),
    ("&lt;", "<"),
    ("&gt;", ">"),
    ("&laquo;", "<<"),
    ("&raquo;", ">>"),
    ("&#039;", "'"),
    ("&#8220;", "\""),
    ("&#8221;", "\""),
    ("&#8216;", "\'"),
    ("&#8217;", "\'"),
    ("&#9632;", ""),
    ("&#8226;", "-")]


def ENMLToHTML(content, pretty=True, header=True, url:str = ''):
    """
    converts ENML string into HTML string
    :param header: If True, note is wrapped in a <HTML><BODY> block.
    :type header: bool
    :param media_filter: optional callable object used to filter undesired resources.
    Returns True if the resource must be kept in HTML, False otherwise.
    :type media_fiter: callable object with prototype: `bool func(hash_str, mime_type)`
    """
    soup = BeautifulSoup(content, "html.parser")

    todos = soup.find_all('en-todo')
    for todo in todos:
        checkbox = soup.new_tag('input')
        checkbox['type'] = 'checkbox'
        checkbox['disabled'] = 'true'
        if todo.has_attr('checked'):
            checkbox['checked'] = todo['checked']
        todo.replace_with(checkbox)

    # if 'media_filter' in kwargs:
    #     media_filter = kwargs['media_filter']
    #     for media in filter(
    #         lambda media: not media_filter(media['hash'], media['type']),
    #         soup.find_all('en-media')):
    #         media.extract()


    # res_folder = os.path.join(folder, 'resources')
    # # 下载资源文件
    # if resourcesList is not None:
    #     for res in resourcesList:
    #         resource_url = DownloadResource(res, res_folder)

    # 替换资源标签
    all_media = soup.find_all('en-media')
    for media in all_media:
        mime_type = media['type']
        if mime_type not in MIME_TO_EXTESION_MAPPING:
            continue
        #resource_url = os.path.join('resources', media['hash'] + MIME_TO_EXTESION_MAPPING[mime_type])
        resource_url = url + '/' + media['hash'] + MIME_TO_EXTESION_MAPPING[mime_type]
        new_tag = soup.new_tag('img')
        new_tag['src'] = resource_url
        media.replace_with(new_tag)

    note = soup.find('en-note')
    if note:
        if header:
            html = soup.new_tag('html')
            html.append(note)
            note.name = 'body'
        else:
            html = note
            note.name = 'div'

        output = html.prettify().encode('utf-8') if pretty else str(html)
        return output

    return content


def DownloadResource(resource: Types.Resource, folder: str) -> str:
    if not os.path.exists(folder):
        os.makedirs(folder)

    mime_type = resource.mime
    if mime_type not in MIME_TO_EXTESION_MAPPING:
        return None

    bodyHash = resource.data.bodyHash
    hash_hex = binascii.hexlify(bodyHash)
    hash_str = hash_hex.decode("UTF-8")
    data = resource.data.body
    # file_path = folder + '/' + hash_str + MIME_TO_EXTESION_MAPPING[mime_type]

    file_name = hash_str + MIME_TO_EXTESION_MAPPING[mime_type]
    file_path = os.path.join(folder, file_name)
    with open(file_path, 'wb') as f:
        f.write(data)
    # return "file://" + file_path
    return file_path


def images_media_filter(hash_str, mime_type):
    """Helper usable with `ENMLToHTML` `media_filter` parameter to filter-out
    resources that are not images so that output HTML won't contain
    such invalid element <IMG src="path/to/document.pdf/>
    """
    return mime_type in MIME_TO_EXTESION_MAPPING
