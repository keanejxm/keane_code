#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
MySQL数据处理。
# author: Trico
# date: 2019.8.15
# update: 2019.8.15
"""

import json
import time
import pymysql
import datetime


class MySQLUtils(object):

    def __init__(self, **config):
        """
        MySQL工具集。
        """

        # 连接MySQL。
        config["charset"] = "utf8mb4"
        config["cursorclass"] = pymysql.cursors.DictCursor
        self.conn = pymysql.connect(**config)

    def __del__(self, *args, **kwargs):
        """
        删除对象时关闭连接，释放资源。
        :return:
        """

        # noinspection PyBroadException
        try:
            self.conn.close()
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()

    @staticmethod
    def _format(values):
        """
        格式化待加载数据（MySQL）。
        :return:
        """

        # 参数验证。
        assert values and isinstance(values, (tuple, list)), "Error param, values."

        new_values = list()
        for value in values:
            if value is None:
                new_values.append("NULL")
            elif isinstance(value, (int, float)):
                new_values.append("{}".format(value))
            elif isinstance(value, (str, bytes)):
                if isinstance(value, bytes):
                    value = value.decode("utf-8")
                value = pymysql.escape_string(value)
                new_values.append("'{}'".format(value))
            elif isinstance(value, datetime.datetime):
                new_values.append("'{}'".format(value.strftime("%Y-%m-%d %H:%M:%S")))
            elif isinstance(value, time.struct_time):
                new_values.append("'{}'".format(time.strftime("%Y-%m-%d %H:%M:%S", value)))
            elif isinstance(value, (dict, list)):
                value = json.dumps(value)
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

    def search(self, sql):
        """
        查询。
        :return:
        """

        # 参数验证。
        assert sql and isinstance(sql, str) and sql.lower().strip().startswith("select"), "Error params, sql."

        # 测试链接。
        self.conn.ping()
        with self.conn.cursor() as cur:
            # 保证字典有序。
            cur.execute(sql)
            return cur.fetchall()

    def update(self, table_name, field_id, fields):
        """
        更新。
        :return:
        """

        # 参数验证。
        assert table_name and field_id and fields, "Error params."

        # 测试链接。
        self.conn.ping()
        # 整合更新内容。
        with self.conn.cursor() as cur:
            # 保证字典有序。
            fields = list(fields.items())
            keys = [value[0] for value in fields]
            values = [value[1] for value in fields]
            values = self._format(values)
            fields = ['{}={}'.format(key, value) for key, value in zip(keys, values)]
            fields_str = ", ".join(fields)
            sql = "update {} set {} where id='{}';".format(table_name, fields_str, field_id)
            cur.execute(sql)

        # 提交。
        self.conn.commit()

    def insert(self, table_name, fields):
        """
        将数据存入mysql。
        :return:
        """

        # 参数验证。
        assert table_name and fields, "Error params."

        # 测试链接。
        self.conn.ping()
        # 整合加载内容。
        with self.conn.cursor() as cur:
            # 保证字典有序。
            fields = list(fields.items())
            keys_str = ", ".join([value[0] for value in fields])
            values = [value[1] for value in fields]
            values = self._format(values)
            values_str = ", ".join(values)
            sql = "insert into {}({}) values({});".format(table_name, keys_str, values_str)
            cur.execute(sql)

        # 提交。
        self.conn.commit()
