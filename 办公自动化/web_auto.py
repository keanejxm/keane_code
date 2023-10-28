#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  web_auto.py
:time  2023/9/15 15:37
:desc  
"""
import asyncio
from pyppeteer import launch
import random


def screen_size():
    # 使用tkinter获取屏幕大小
    import tkinter
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return width, height


async def main():
    width, height = screen_size()
    browser = await launch(
        headless=False,
        userDataDir='./userdata',
        executablePath=r"C:\Users\keane\AppData\Local\Google\Chrome\Application\chrome.exe",
        args=[
            "--disable-infobars",
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',  # 不添加无法加载iframe内容
            f'--window-size={width},{height}'])
    page = await browser.newPage()
    print(width, height)
    # 设置窗口大小
    await page.setViewport(viewport={"width": width, "height": height})
    # 是否启用js，enabled设为False,则无渲染效果
    await page.setJavaScriptEnabled(enabled=True)
    await page.evaluateOnNewDocument('Object.defineProperty(navigator, "webdriver", {get: () => false })')
    await page.goto("https://b.mybank.cn/index.htm#/login?loginType=ukey", options={"timeout": 5 * 1000})
    # await page.goto("https://uland.taobao.com/", options={"timeout": 5 * 1000})
    await asyncio.sleep(10)

    # 获取网页内容
    page_text = await page.content()
    print(page_text)
    input("回车继续")
    # 屏幕截图
    # await page.screenshot({"path":"example1.png"})

    # 添加useragent
    # await page.setUserAgent('')

    # 获取输入框焦点并输入文字
    # await page.type("#kw","keyword",{"delay":100})

    # 鼠标点击
    # await page.click("#ant-btn ant-btn-primary ant-btn-lg login___16KCu")

    # 等待页面加载出来
    # await page.waitForNavigation({"waitUntil": "load"})

    # 获取cookie
    cookies = await page.cookies()
    print(cookies)
    input("结束")
    # 在网页中执行js代码
    # await page.evaluate("js1")

    # 模拟键盘按下某个按键
    # await page.keyboard.press()

    # 页面等待，可以是时间、某个元素、某个函数
    # await page.waitFor()

    # 获取当前访问的url
    # page_url = await page.url

    # 获取iframe中的某个元素
    # await iframe.$("")

    # await asyncio.sleep(random.randint(1,3))
    # await page.screenshot({"path":"example2.png"})
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())

