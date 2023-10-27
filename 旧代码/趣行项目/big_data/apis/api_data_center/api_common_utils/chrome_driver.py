# -*- coding:utf-8 -*-
"""
Chrome Driver。
# author: Trico
# date: 2020.6.3
# update: 2020.6.3
"""

import traceback
from selenium import webdriver
from pyvirtualdisplay import Display
from api_common_utils.proxy import create_proxy_auth_extension


class ChromeDriver(object):

    def __init__(self, timeout=50):
        # 参数验证。
        assert isinstance(timeout, (int, float)) and timeout > 0, "Error param, timeout."
        self._timeout = timeout

        # 虚拟屏幕列表。
        self._running_display_list = list()
        # webdriver列表。
        self._running_driver_list = list()

    def __del__(self):
        """
        释放对象占用的资源。
        :return:
        """

        if self._running_display_list:
            for display in self._running_display_list:
                # noinspection PyBroadException
                try:
                    display.stop()
                except Exception:
                    pass
        if self._running_driver_list:
            for driver in self._running_driver_list:
                # noinspection PyBroadException
                try:
                    driver.quit()
                except Exception:
                    pass

    def start_display(self, logger):
        """
        启动虚拟图形界面。
        :return:
        """

        # 开启一个虚拟显示界面。
        try:
            display = Display(visible=0, size=(1920, 1080))
            display.start()
            # 队列追加。
            self._running_display_list.append(display)
            return display
        except Exception as e:
            if "server already running" in str(e):
                logger.debug("{}\n{}".format(e, traceback))
            else:
                raise

    def get_driver(self, use_proxy=False):
        """
        获取WebDriver。
        :return:
        """

        # WebDriver配置信息及会话。
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument('lang=zh_CN.UTF-8')
        # 禁止图片加载。
        options.add_argument('blink-settings=imagesEnabled=false')
        # 禁止图片加载。
        prefs = {
            "profile.default_content_setting_values": {
                "images": 2,
                "notifications": 2
            }
        }
        options.add_experimental_option("prefs", prefs)

        # 是否开启代理。
        if use_proxy is True:
            # 获取代理服务。
            proxy_auth_plugin_path = create_proxy_auth_extension()
            options.add_extension(proxy_auth_plugin_path)

        # WebDriver会话。
        driver = webdriver.Chrome(
            # executable_path="/usr/local/chromedriver",
            # executable_path="/bin/chromedriver",
            # executable_path="E:/trico/Python3.6.4_64bit/chromedriver_win32_81.0.4044.69.exe",
            options=options,
        )
        # 隐藏webdriver属性，避免被某些网站识破。
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
        driver.set_page_load_timeout(self._timeout)
        driver.set_script_timeout(self._timeout)
        driver.implicitly_wait(self._timeout)

        # 队列追加。
        self._running_driver_list.append(driver)

        return driver


def test():
    import time
    # 测试。
    chrome = ChromeDriver()
    driver = chrome.get_driver()
    # del chrome
    # driver.get("https://weibo.com/")
    # time.sleep(5)
    # driver.find_element_by_xpath("//a[@node-type='loginBtn' and text()='登录']").click()
    # print()
    try:
        driver.get("https://www.baidu.com/")
        print(driver.page_source)
    finally:
        driver.quit()
        del chrome


if __name__ == "__main__":
    test()
