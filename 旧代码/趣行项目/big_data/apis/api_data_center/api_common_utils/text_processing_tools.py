# -*- coding:utf-8 -*-
"""
文本处理： 文本分割 、 文本去除HTML标签 、 判断文本长度
# author: albert
# date: 2020/12/9
# update: 2020/12/9
"""
import re
from bs4 import BeautifulSoup
from lxml import etree


def get_text_byte_length(text: str) -> int:
    """
    接收一个文本 字符串类型  返回文本的字节长度
    """
    if isinstance(text, str):
        return len(str(text).encode('utf-8'))
    raise ValueError(f'这是获取文本的字节长度， 你传的是-{type(text)}-的类型，大神！请传-字符串-类型的数据好吗?')


def text_remover_symbol(html: str) -> str:
    """
    去除标点符号
    """
    punc = '~`!#$%^&*()_+-=|\';":/.,?><~·！@#￥%……&*（）——+-=“”：’；、。，？》《{}'
    return re.sub(r"[%s]+" % punc, "", html).replace(' ', '')


def text_remover_html_tag(html: str, method: str = 'bs4') -> str:
    """
    接收一个网页文本 字符串类型  返回去除HTML标签后的文本
    """
    if not isinstance(html, str):
        raise ValueError('我这是去除文本中HTML标签的， 你不传字符串， 你传个是个视频吗?~')
    if not isinstance(method, str):
        raise ValueError('选择去除的方法 是字符串类型， 填写 re 或者 bs4 或者 xpath')
    if method not in ('re', 'bs4', 'xpath'):
        raise ValueError('不都告诉你了， 填写re 或者 bs4 或者 xpath')
    html = "".join(html.split())
    # 正则提取文本
    if method == 're':
        pattern1 = re.compile(r'<[^>]+>', re.S)
        result1 = pattern1.sub('', html)
        pattern = re.compile(r'<script.*?</script>', re.S)
        result = pattern.sub('', result1)
        return result
    # BeautifulSoup提取文本
    if method == 'bs4':
        soup = BeautifulSoup(html, 'html.parser')
        soup = BeautifulSoup(soup.get_text(), 'html.parser')
        return soup.get_text()
    # Xpath提取文本
    if method == 'xpath':
        response = etree.HTML(text=html)
        return response.xpath('string(.)')
    raise ValueError('不都告诉你了， 填写re 或者 bs4 或者 xpath')


def text_segmentation(text: str, method: str = 'complete', length: int = 65535) -> list:
    """
    文本分割
        text： 字符串文本
        method : 分割方法  str 或者 byte 默认byte
        length : 分割的长度 默认 65535
    """
    if not isinstance(text, str):
        raise ValueError('传入的不是字符串')
    if not isinstance(method, str):
        raise ValueError('选择去除的方法 是字符串， 填写re 或者 bs4 或者 xpath')
    if method not in ('str', 'byte', 'complete'):
        raise ValueError('不都告诉你了， str 或者 byte 或者 complete')
    if method == 'str':
        text_list = re.findall(r'.{' + str(length) + '}', text)
        text_list.append(text[(len(text_list) * length):])
        return text_list
    if method == 'byte':
        text_byte = text.encode('utf-8')
        ls = [text_byte[i:i + length] for i in range(len(text_byte)) if i % length == 0]  # 每3个字节分隔组成list
        return ls
    if method == 'complete':
        res = []
        start = 0
        for i in range(int(len(text) / length) + 3):
            sp_index = text[start:start + length].rfind('。') + 1
            r = text[start:start + sp_index]
            start = start + sp_index
            if r:
                res.append(r)
        return res
    raise ValueError('不都告诉你了， str 或者 byte 或者 complete')

