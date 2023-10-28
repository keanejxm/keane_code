#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  pyppeteer_test.py
:time  2023/9/18 16:01
:desc  
"""
import asyncio
import copy

from pyppeteer import launch


class TestPyppeteer:
    def __init__(self):
        # 谷歌浏览地址
        self.chrome_extension = ""
        self.launch_kwargs = {
            # 控制是否为无头模式
            "executablePath": self.chrome_extension,  # 文件目录位置
            "headless": True,  # 控制是否为无头模式
            "dumpio": True,  # 当界面开多了时会卡住，设置这个参数就不会了
            "userDataDir": "./userdata",  # 用户数据保存目录
            "autoClose": True,
            # chrome启动命令行参数
            "args": [
                # 浏览器代理 配合某些中间人代理使用
                # "--proxy-server=http://127.0.0.1:8008",
                # 最大化窗口
                "--start-maximized",
                # 窗口大小
                "--window-size=1366,768",
                # 取消沙盒模式
                "--no-sandbox",
                # 不显示信息栏，比如chrome正在收到自动测试软件的控制
                "--disable-infobars",
                # log登记设置
                "--log-level=3",
                # 设置ua
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            ]
        }

    def __del__(self):
        asyncio.gather(self.browser.close())  # 爬虫程序结束，关闭browser对象
        print("程序结束")

    async def run(self):
        item = dict()
        url_list = [""]
        temp_url = ""
        for i in range(2, 10):
            url_list.append(temp_url.format(i))
        self.browser = await launch(self.launch_kwargs)
        page = await self.browser.newPage()
        await page.evaluateOnNewDocument(
            '() =>{Object.defineProperties(navigator,""{"webdriver":{get: () => false }})}')
        await page.setUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 "
            "Safari/537.36"
        )
        for url in url_list:
            await page.goto(url, waitUntil="networkidle0")  # 等待网页加载完成
            # 利用xpath语法提取数据
            item_list = []
            item["detail_url"] = url
            a_list = page.xpath("")
            for i in a_list:
                title = await (await i.getProperty("textContent")).jsonValue()
                get_url = await (await i.getProperty("href")).jsonValue()
                item["title"], item["get_url"] = str(title).strip(), get_url
            if item_list:
                await self.get_detail_parse(page, copy.deepcopy(item_list))

    async def get_detail_parse(self, page, item_list):
        """"""
        for item in item_list:
            await page.goto(item["get_url"], waitUntil="networidle0")
            a_list = await page.xpath("")
            content_data = await page.content()
            for i in a_list:
                item["name"] = await (await i.getProperty("textContent")).jsonValue()
                item["url"] = await (await i.getProperty("href")).jsonValue()


if __name__ == '__main__':
    func = TestPyppeteer()
    asyncio.run(func.run())
