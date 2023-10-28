#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
工具组。
# author: Trico
# date: 2020.1.10
# update: 2020.1.10
"""

import tldextract
custom_cache_extract = tldextract.TLDExtract()


def get_primary_domain(url):
    """
    获取URL中的主域名。
    :return:
    """

    ext = custom_cache_extract(url)
    return "{}.{}".format(ext.domain, ext.suffix)
