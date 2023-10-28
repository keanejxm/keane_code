# -*- coding:utf-8 -*-
"""
电子报模板。
# author: Neil
# date: 2020/12/2
# update: 2020/12/2
"""

import pymysql
import traceback
import json
from api.config import mysql_config


class EPaperTemplate(object):

    def __init__(self, logger):
        self._logger = logger

    def create(self, template_info):
        """
        新增电子报采集模板。
        1、先查再加
        :return:
        """
        assert "templates" and isinstance(template_info, dict), "Error param, data"
        paper_templates = template_info["templates"]
        assert isinstance(paper_templates, list), "Error param, paper_templates"
        conmysql = pymysql.connect(**mysql_config)
        cursor = conmysql.cursor()
        for paper_template in paper_templates:
            try:
                name = paper_template["platformName"]
                paper_template["platformType"] = 6
                source_level = paper_template["sourceLevel"]
                source_classify = paper_template["sourceClassify"]
                source_importance = paper_template["sourceImportance"]
                media = paper_template['mainMedia']
                paper_template = json.dumps(paper_template)
                # 先查询是否存在
                sql = f"select platformName from epaper_template where platformName='{name}';"
                try:
                    cursor.execute(sql)
                except Exception as e:
                    self._logger.warning("{}\n{}".format(e, traceback.format_exc()))
                mysql_result = cursor.fetchall()
                if mysql_result:
                    self._logger.debug(f"该'{name}'已存在")
                    continue
                else:
                    # 将数据写入到数据库
                    sql = 'insert into epaper_template (platformName, platformType, sourceLevel, sourceClassify, ' \
                          'sourceImportance, mainMedia, epaperTemplate) values (%s,6,%s,%s,%s,%s,%s)'
                    data = (name, source_level, source_classify, source_importance, media, paper_template)
                    try:
                        cursor.execute(sql, data)
                        conmysql.commit()
                        self._logger.debug(f"该'{name}'添加成功")
                    except Exception as e:
                        conmysql.rollback()
                        self._logger.warning("{}\n{}".format(e, traceback.format_exc()))
            except Exception as e:
                self._logger.warning("{}\n{}".format(e, traceback.format_exc()))
                continue
        cursor.close()
        conmysql.close()
        return {"message": "Add successfully"}

    def delete(self, newspaper_name):
        """
        删除数据库模板信息
        通过报纸名字进行删除模板
        1、先查再删
        :param newspaper_name:
        :return:
        """
        assert "templates" and isinstance(newspaper_name, dict), "Error param, data"
        paper_templates = newspaper_name["templates"]
        assert isinstance(paper_templates, list), "Error param, paper_templates"
        conmysql = pymysql.connect(**mysql_config)
        cursor = conmysql.cursor()
        for paper_template in paper_templates:
            try:
                name = paper_template["platformName"]
                # 先查询是否存在
                sql = f"select platformName from epaper_template where platformName='{name}';"
                try:
                    cursor.execute(sql)
                except Exception as e:
                    self._logger.warning("{}\n{}".format(e, traceback.format_exc()))
                mysql_result = cursor.fetchall()
                if mysql_result:
                    sql = f"delete from epaper_template where platformName='{name}';"
                    try:
                        cursor.execute(sql)
                        conmysql.commit()
                        self._logger.debug(f"该'{name}'删除成功")
                    except Exception as e:
                        conmysql.rollback()
                        self._logger.warning("{}\n{}".format(e, traceback.format_exc()))
                else:
                    continue
            except Exception:
                continue
        cursor.close()
        conmysql.close()
        return {"message": "Delete successfully"}

    def update(self, template_info):
        """
        更新数据库模板信息
        1、先查再更新
        :param template_info:
        :return:
        """
        assert "templates" and isinstance(template_info, dict), "Error param, data"
        paper_templates = template_info["templates"]
        assert isinstance(paper_templates, list), "Error param, paper_templates"
        conmysql = pymysql.connect(**mysql_config)
        cursor = conmysql.cursor()
        for paper_template in paper_templates:
            try:
                name = paper_template["platformName"]
                source_level = paper_template["sourceLevel"]
                source_classify = paper_template["sourceClassify"]
                source_importance = paper_template["sourceImportance"]
                media = paper_template['mainMedia']
                paper_template = str(paper_template)
                # 先查询是否存在
                sql = f"select platformName from epaper_template where platformName='{name}';"
                try:
                    cursor.execute(sql)
                except Exception as e:
                    self._logger.warning("{}\n{}".format(e, traceback.format_exc()))
                mysql_result = cursor.fetchall()
                if mysql_result:
                    sql = "UPDATE epaper_template SET epaperTemplate=%s, sourceLevel=%s,sourceClassify=%s," \
                          "sourceImportance=%s, mainMedia=%s where platformName=%s"
                    val = (paper_template, source_level, source_classify, source_importance, media, name)
                    try:
                        cursor.execute(sql, val)
                        conmysql.commit()
                        self._logger.debug(f"该'{name}'更新成功")
                    except Exception as e:
                        self._logger.warning("{}\n{}".format(e, traceback.format_exc()))
                        conmysql.rollback()  # 发生错误时回滚
                        raise Exception('query error')
                else:
                    pass
            except Exception:
                continue
        cursor.close()
        conmysql.close()
        return {"message": "Update successfully"}
