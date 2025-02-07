#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  aaaaa.py
:time  2025/1/24 11:20
:desc  
"""
import asyncio

import aiohttp
from aiohttp import ClientSession


async def fetch(session, url):
    async with session.get(url) as response:
        return response.text


async def post(session, url):
    async with session.post(url) as response:
        return await response.text()


async def main():
    with aiohttp.ClientSession() as session:
        html = await fetch(session, "https://keane.github.io/keane-python/docs/")

asyncio.run(main())