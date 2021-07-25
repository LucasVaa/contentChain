# -*- coding:UTF-8 -*-
"""
Created on 2021年3月16日

@author: Xinhuiyang
实现内容对象数据本地文件系统存取中需要调用的方法，包括：
    1)generate_identity，生成内容唯一标识cid
    2)convert，将十进制内容标识转换成8位32进制字符编码
    3)mkdir，根据cid生成内容对象数据存储目录
    4)content_hash，根据内容对象数据生成内容哈希
    5)content_node_choose，内容对象数据存储时，选择内容结点从结点备份内容对象数据
"""
import os
import hashlib
import random
import sys
sys.path.append(os.pardir)
from fastAPIServer.routers.ca import ca_node


epub_lib = '/home/ubuntu/content/storage'# from contentDb import createTable
# from playhouse.shortcuts import model_to_dict

# epub_lib = '/home/lucas/ubuntu/content/storage'

def generate_identity(cid):
    """
    Generated unique identification of content.

    Args:
        db: Database instance to store unique identification of content.

    Returns:
        Unique identification of content
    """
    if(cid == ''):
        cid = 0
        cid = convert(cid)
        return cid
    else:
        list_a = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
              'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K',
              'L', 'M', 'N', 'P', 'Q', 'R', 'T', 'U', 'V', 'W', 'X', 'Y']
        list_b = list(cid)
        length = len(list_b)
        cid = 0
        for i in range(length):
            cid += list_a.index(list_b[i]) * pow(32, length - i - 1)
        cid += 1
        cid = convert(cid)
        return cid

def convert(cid):
    """
    Convert cid to 32 base.

    Args:
        cid: Unique identification of content on the contentChain.

    Returns:
        32 base content identification.
    """
    list_a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D',
              'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P',
              'Q', 'R', 'T', 'U', 'V', 'W', 'X', 'Y']
    list_b = []
    list_c = []
    a = ''
    while True:
        s = cid//32
        y = cid % 32
        list_b.append(y)
        if s == 0:
            break
        cid = s
    for i in range(8-len(list_b)):
        list_b.append(0)
    list_b.reverse()
    for i in list_b:
        list_c.append(list_a[i])
    for i in range(len(list_c)):
        a = a + str(list_c[i])
    return a


def mkdir(cid):
    """
    Create a directory to store content object data according to cid.

    Args:
        cid: 32 base content identification.

    Returns:
        Storage path of content object data.
    """
    a = cid[0:2]
    b = cid[2:4]
    c = cid[4:6]
    d = cid[6:8]
    path = epub_lib + '/' + a + '/' + b + '/' + c + '/' + d + '/'
    exists = os.path.exists(path)
    if not exists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return path
    return path


def content_hash(obj):
    """
    Using MD5 algorithm to generate content hash.

    Args:
        obj: Content object data.

    Returns:
        Content hash.
    """
    d = hashlib.md5()
    d.update(obj)
    return d.hexdigest()
