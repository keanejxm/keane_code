#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
电子报模板，测试、上传及更新接口。
2019年12月19日，更新，加入检查功能。
# author: Trico
# date: 2019.11.29
# update: 2019.12.19
"""

import json
import time
import pymysql
import datetime

from custom_website.api_website_check import WebsiteSpider
from api_common_utils.llog import LLog


class WebsiteTemplate(object):

    def __init__(self, logger=None):
        """
        接口。
        """

        # 日志对象。
        if logger:
            self._logger = logger
        else:
            self._logger = LLog("website_template", log_path="./logs").logger

        # 表名。
        self._table_name = "website"

        # 链接MySQL。
        self._db = self.conn_mysql()

    def __del__(self):
        # noinspection PyBroadException
        try:
            self._db.close()
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self):
        self.__del__()

    @staticmethod
    def fault(msg):
        """
        失败返回值。
        :return:
        """

        return dict(
            code=0,
            msg=msg,
        )

    @staticmethod
    def succ(msg):
        """
        成功返回值。
        :return:
        """

        return dict(
            code=1,
            msg=msg,
        )

    @staticmethod
    def conn_mysql():
        config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'passwd': 'moR7tzWCv$ZYBe*$',
            'db': 'big_data',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        return pymysql.connect(**config)

    @staticmethod
    def format_values(values):
        """
        格式化待加载数据（MySQL）。
        :return:
        """

        if not isinstance(values, (tuple, list)):
            raise TypeError("The insert values({}) is not a type of list/tuple.".format(type(values)))

        new_values = list()
        for value in values:
            if value is None:
                new_values.append("NULL")
            elif isinstance(value, (int, float)):
                new_values.append("{}".format(value))
            elif isinstance(value, (str, bytes)):
                if isinstance(value, bytes):
                    value = value.decode('utf-8')
                value = pymysql.escape_string(value)
                new_values.append("'{}'".format(value))
            elif isinstance(value, datetime.datetime):
                new_values.append("'{}'".format(value.strftime("%Y-%m-%d %H:%M:%S")))
            elif isinstance(value, time.struct_time):
                new_values.append("'{}'".format(time.strftime("%Y-%m-%d %H:%M:%S", value)))
            elif isinstance(value, (dict, list)):
                value = json.dumps(value, separators=(',', ':'))
                value = pymysql.escape_string(value)
                new_values.append("""'{}'""".format(value))
            else:
                # noinspection PyBroadException
                try:
                    value = repr(value)
                except Exception:
                    new_values.append("''")
                    continue
                value = pymysql.escape_string(value)
                new_values.append("'{}'".format(value))

        return new_values

    @staticmethod
    def prepare(data):
        """
        数据准备。
        :return:
        """

        # 基本参数。
        if "platformName" not in data or not data["platformName"]:
            raise ValueError("Param error: platformName.")

        # 来源省份。
        source_province = ""
        if "sourceProvince" in data:
            source_province = data["sourceProvince"]

        # 来源城市。
        source_city = ""
        if "sourceCity" in data:
            source_city = data["sourceCity"]

        # 来源区县。
        source_county = ""
        if "sourceCounty" in data:
            source_county = data["sourceCounty"]

        # 来源级别。
        source_level = -1
        if "sourceLevel" in data:
            source_level = data["sourceLevel"]
        # 来源类别。
        source_classify = -1
        if "sourceClassify" in data:
            source_classify = data["sourceClassify"]

        # 重点渠道。
        source_importance = -1
        if "sourceImportance" in data:
            source_importance = data["sourceImportance"]

        # 主流媒体。
        mainmedia = -1
        if "mainMedia" in data:
            mainmedia = data["mainMedia"]

        # 各级分类。
        category_first = ""
        if "categoryFirst" in data:
            category_first = data["categoryFirst"]
        category_second = ""
        if "categorySecond" in data:
            category_second = data["categorySecond"]
        category_third = ""
        if "categoryThird" in data:
            category_third = data["categoryThird"]

        # 采集参数。
        params = dict()
        if "params" in data:
            params = data["params"]

        # 模板数据。
        templates = list()
        if "templates" in data:
            templates = data["templates"]
            status = 1
        else:
            status = 0

        # 状态，一般涉及到是否采集该站。
        # noinspection PyBroadException
        try:
            if "status" in data:
                status = data["status"]
                assert status in (0, 1), "Error param, status."
        except Exception:
            pass

        fields = dict(
            platformName=data["platformName"],
            platformType=5,
            sourceProvince=source_province,
            sourceCity=source_city,
            sourceCounty=source_county,
            sourceLevel=source_level,
            sourceClassify=source_classify,
            sourceImportance=source_importance,
            mainMedia=mainmedia,
            categoryFirst=category_first,
            categorySecond=category_second,
            categoryThird=category_third,
            rankCoefficient=1.0,
            status=status,
            spiderType=1,
            params=json.dumps(params, separators=(',', ':')),
            templates=json.dumps(templates, separators=(',', ':')),
        )

        return fields

    def get_website_id_from_db(self, table_name, platform_name=None, _id=None):
        """
        判断名称是对应的ID。
        :return:
        """

        # 参数验证。
        assert platform_name or _id, "Error param, platform_name or _id."

        # 判断名称是否已存在。
        if _id:
            sql = "select id from {} where id = '{}' limit 1".format(table_name, _id)
        elif platform_name:
            sql = "select id from {} where platformName = '{}' limit 1".format(table_name, platform_name)
        else:
            raise ValueError("Error param, platform_name or _id.")

        # 执行检索。
        with self._db.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchone()
            if res and len(res) > 0:
                return res["id"]
            else:
                return None

    def is_exist(self, table_name, platform_name=None, _id=None):
        """
        判断名称是否已存在。
        :return:
        """

        return self.get_website_id_from_db(table_name, platform_name, _id)

    def update(self, data):
        """
        更新数据。
        :return:
        """

        # 参数验证。
        assert data and isinstance(data, dict), "Error param, data."

        # 赋值时间。
        now = datetime.datetime.now().strftime("%Y:%m:%d %H:%M:%S.%f")
        data["updateTime"] = now

        # 保证字典有序。
        fields = list(data.items())
        # 字段名。
        keys = [value[0] for value in fields]
        # 字段值。
        values = [value[1] for value in fields]
        values = self.format_values(values)
        # 更新字段。
        fields = ['{}={}'.format(key, value) for key, value in zip(keys, values)]
        set_clause = ', '.join(fields)

        # 更新语句。
        sql = "update {table} set {set_clause} where platformName='{platform_name}';".format(
            table=self._table_name, set_clause=set_clause, platform_name=data["platformName"]
        )

        # 执行更新。
        with self._db.cursor() as cursor:
            cursor.execute(sql)
        self._db.commit()

        # 返回成功。
        ret = dict(
            msg='Update OK.',
            code=1,
        )
        return ret

    def create(self, data):
        """
        创建数据。
        :return:
        """

        # 参数验证。
        assert data and isinstance(data, dict), "Error param, data."

        # 检查是否已存在，存在时则更新。
        resp = self.is_exist(self._table_name, data["platformName"])
        if resp is not None:
            return self.update(data)

        # 赋值时间。
        now = datetime.datetime.now().strftime("%Y:%m:%d %H:%M:%S.%f")
        data["createTime"] = data["updateTime"] = now

        # 保证字典有序。
        fields = list(data.items())
        # 字段名。
        keys_str = ', '.join([value[0] for value in fields])
        # 字段值。
        values = [value[1] for value in fields]
        values = self.format_values(values)
        values_str = ', '.join(values)
        # 加载语句。
        sql = "insert into {}({}) values({});".format(self._table_name, keys_str, values_str)
        # 执行加载。
        with self._db.cursor() as cursor:
            cursor.execute(sql)
        self._db.commit()

        ret = dict(
            msg='Insert OK.',
            code=1,
        )
        return ret

    def check(self, data, batch_size=10):
        """
        测试模板爬取效果。
        :return:
        """

        # 先创建（或更新）条目。
        ret = self.create(data)
        if ret["code"] != 1:
            yield ret

        # 查询数据库里的内容。
        sql = "select * from {} where platformName='{}' limit 1;".format(self._table_name, data["platformName"])
        with self._db.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchone()

        # 遍历结果集。
        ws_obj = WebsiteSpider(row, logger=self._logger)
        for batch in ws_obj.fetch_batch(batch_size=batch_size, check_mode=True):
            yield dict(
                msg="OK",
                code=1,
                naviLinks=ws_obj.exist_navi_links,
                docList=batch,
            )
