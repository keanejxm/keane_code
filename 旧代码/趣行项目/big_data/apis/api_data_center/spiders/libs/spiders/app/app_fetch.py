# -*- encoding:utf-8 -*-
"""
@功能:app爬虫运行采集接口
@AUTHOR：Keane
@文件名：app_fetch.py
@时间：2020/12/28  11:02
"""

import importlib
import traceback
from api_common_utils.llog import LLog


class AppFetch(object):

    @staticmethod
    def fetch_batch(task, logger):
        """
        获取批结果。
        :return:
        """

        try:
            app_name = task["platformName"]
            platform_id = task["platformID"]
            self_typeid = task["selfTypeIDs"]
            func_name = task["pyName"]
            func_name = f"spiders.libs.spiders.app.app_analysis_model.{func_name}"
            module = importlib.import_module(func_name)
            module = importlib.reload(module)
            logger.info(f"Module '{func_name}'({module.__file__}): {app_name}.")
            app_data = module.fetch_batch(app_name, logger, platform_id, self_typeid)
            return app_data
        except Exception as e:
            logger.error(f"{e}\n{traceback.format_exc()}")
            return dict(code=0, msg=str(e))

    @staticmethod
    def fetch_yield(task, logger):
        """
        获取流结果。
        :return:
        """

        try:
            app_name = task["platformName"]
            platform_id = task["platformID"]
            self_typeid = task["selfTypeIDs"]
            func_name = task["pyName"]
            func_name = f"spiders.libs.spiders.app.app_analysis_model.{func_name}"
            module = importlib.import_module(func_name)
            module = importlib.reload(module)
            logger.info(f"Module '{func_name}'({module.__file__}): {app_name}.")
            # 流数据返回
            yield from module.fetch_yield(app_name, logger, platform_id, self_typeid)
        except Exception as e:
            logger.error(f"{e}\n{traceback.format_exc()}")
            yield dict(code=0, msg=str(e))


def run():
    task = {
        "platformName": "环球Time移动端",
        "platformID": "ae5c255e29f53879ec1ae3e581c6c416",
        "selfTypeIDs": "4_3_11",
        "pyName": "huan_qiu_time",
    }
    app_fet = AppFetch()
    logger = LLog("APP客户端", only_console=True, logger_level="INFO").logger
    generator = app_fet.fetch_yield(task, logger)
    for data in generator:
        print(data)


if __name__ == '__main__':
    run()
