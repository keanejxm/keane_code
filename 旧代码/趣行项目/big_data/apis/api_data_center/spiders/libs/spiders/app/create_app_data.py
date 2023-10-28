#!/usr/bin/env python3
# -*- coding:utf-8
# Author Keane
# coding=utf-8
# @Time    : 2021/1/15 17:48
# @File    : create_app_data.py
# @Software: PyCharm
import importlib
from api_common_utils.llog import LLog
from spiders.libs.spiders.app.es_untils import EsUtils
import pymysql


class AppFetch(object):
    def __init__(self):
        self._es_utils = EsUtils()

    def app_fetch(self, task, logger):
        app_name = task.get("platformName")
        platform_id = task.get("platformID")
        self_typeid = task.get("selfTypeIDs")
        print(self_typeid)
        try:
            func_name = task["value"]["pyName"]
            func_name = f"spiders.libs.spiders.app.app_analysis_model.{func_name}"
            module = importlib.import_module(func_name)
            module = importlib.reload(module)
            app_data = module.fetch_yield(app_name, logger, platform_id, self_typeid)
            for data in app_data:
                if "channel" in data["data"]:
                    channel = data["data"]["channel"]
                    res = self._es_utils.api_create_channel(channel)
                    print(res)
                if "works" in data["data"]:
                    res = self._es_utils.api_create_articel(data["data"]["works"])
                    print(res)
                elif "topic" in data["data"]:
                    res = self._es_utils.api_create_topic(data["data"]["topic"])
                    print(res)
            logger.debug("Module '{}'({}): {}.".format(func_name, module.__file__, app_name))
            # funcs.append(func)
        except Exception:
            # 引入失败时停止执行。
            logger.error("Failed to import '{}'.\n".format(app_name))
            return False


def run():
    mysql_config = {
        "host": "180.76.96.208",
        "port": 3306,
        "user": "debugger",
        "passwd": "903976",
        "db": "data_center",
        "charset": "utf8mb4",
        "cursorclass": pymysql.cursors.DictCursor
    }
    conmysql = pymysql.connect(**mysql_config)
    cursor = conmysql.cursor()
    sql = "select * from app_template"
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        task = {"platformName": result["platformName"], "value": {"pyName": result["app_template"]},
                "platformID": result["platformID"], "selfTypeIDs": result["selftypeID"]}
        app_fet = AppFetch()
        logger = LLog("APP客户端", only_console=True, logger_level="INFO").logger
        app_fet.app_fetch(task, logger)


def test():
    task = {"platformName": "宁夏日报移动端",
            "value": {"pyName": "ningxiaribao"},
            "platformID": "943c53b2e599faf000bcfa5527ae1adb",
            "selfTypeIDs": "4_1_17_6"}
    app_fet = AppFetch()
    logger = LLog("APP客户端", only_console=True, logger_level="INFO").logger
    app_fet.app_fetch(task, logger)


if __name__ == '__main__':
    test()
