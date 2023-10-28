#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
阿部云代理。
# author: Trico
# date: 2019.11.25
# update: 2019.11.25
"""

import os
import json
import gzip
import base64
import string
import zipfile
import requests


def __get_abuyun_proxy_from_api(mode=None):
    """
    从接口中获取阿部云代理配置信息。
    :param mode: mode代表模式，1动态版，2专业版，3经典版。
    :return:
    """

    # 获取随机微博cookie。
    if mode is not None:
        get_abuyun_proxy_url = "http://192.168.16.7:16100/crawler_resources/get_abuyun_proxy"
    elif mode in (1, 3):
        get_abuyun_proxy_url = f"http://192.168.16.7:16100/crawler_resources/get_abuyun_proxy?mode={mode}"
    else:
        get_abuyun_proxy_url = "http://192.168.16.7:16100/crawler_resources/get_abuyun_proxy"
    resp = requests.get(get_abuyun_proxy_url, timeout=10)
    resp_data = json.loads(resp.content)
    proxy_str = resp_data["data"]
    proxy_bytes = base64.standard_b64decode(proxy_str.encode("utf-8"))
    proxy = gzip.decompress(proxy_bytes)
    proxy = json.loads(proxy)

    return proxy


def create_proxy_auth_extension(scheme='http', plugin_path=None, mode=None):
    """
    给webdriver使用的代理，需要在本地目录创建一个代理插件。
    :param scheme: 访问协议。
    :param plugin_path: 插件存放路径。
    :param mode: mode代表模式，1动态版，2专业版，3经典版。
    :return:
    """

    # 阿部云代理配置信息。
    proxy = __get_abuyun_proxy_from_api(mode=mode)
    proxy_meta = proxy["meta"]
    if plugin_path is None:
        plugin_path = f"/opt/data/{proxy_meta['username']}@{proxy_meta['host']}_{proxy_meta['port']}.zip"

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Abuyun Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = string.Template(
        """
        var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                },
                bypassList: ["foobar.com"]
            }
          };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ["blocking"]
        );
        """
    ).substitute(
        host=proxy_meta["host"],
        port=proxy_meta["port"],
        username=proxy_meta["username"],
        password=proxy_meta["password"],
        scheme=scheme,
    )

    # 生成插件。
    os.makedirs(os.path.dirname(plugin_path), exist_ok=True)
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path


def get_abuyun_proxies(mode=None):
    """
    获取阿部云代理，组合成url的样式。
    :param mode: mode代表模式，1动态版，2专业版，3经典版。
    :return:
    """

    # 阿部云代理数据体。
    abuyun_proxy = __get_abuyun_proxy_from_api(mode=mode)
    abuyun_proxies = abuyun_proxy["proxies"]
    return abuyun_proxies
