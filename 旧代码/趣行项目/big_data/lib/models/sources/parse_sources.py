# -*- coding:utf-8 -*-
"""
上传信源模板，源自每个人的统计数据（excel表）。
# author: Trico
# date: 2020/12/16
# update: 2020/12/16
"""

import os
import math
import json
import pandas


class SourceData(object):
    """
    整理人工提取的信源数据。
    """

    def __init__(self):
        self._known_types = {
            "微信数据": "1",
            "微博数据": "2",
            "网站数据": "3",
            "APP数据": "4",
            "报纸数据": "5",
            "论坛数据": "6",
        }
        self._other_known_types = {
            # "微信数据": "1",
            # "微博数据": "2",
            # "网站数据": "3",
            # "APP数据": "4",
            # "报纸数据": "5",
            # "论坛数据": "6",
        }

        self._path_1 = rf"E:/trico/项目/大数据平台/信源模型/人工解析/全部信源_修正版"
        self._path_2 = rf"/home/debugger/neil/big_data/big_data_platform/lib/models/sources/全部信源_程序清洗"
        self._path_3 = rf"/home/debugger/neil/big_data/big_data_platform/lib/models/sources/全部信源_结果"

    def parse_excel_file(self, path):
        """
        读取信源文件。
        :return:
        """

        platform_type = str(os.path.basename(path).split(".")[0])
        file = pandas.ExcelFile(path)
        table = file.parse(sheet_name=0)
        parent = platform_type
        types = {parent: dict(
            id=self._known_types[platform_type],
            name=parent,
            children=0,
            parent=None,
            parent_id=None)
        }
        for i, row in enumerate(table.iterrows()):
            main = is_main = False
            url = ""
            parent = platform_type
            for j, item in enumerate(row[1]):
                if j < 5:
                    if j == 2:
                        main = str(item).strip()
                    elif j == 3:
                        url = str(item).strip()
                        if url == "nan":
                            url = ""
                    elif j == 4:
                        if platform_type != str(item).strip():
                            raise ValueError(f"错误文件（{i}）：{path}")
                    continue
                else:
                    if isinstance(item, float) and math.isnan(item):
                        continue
                item = str(item).strip()
                if item == main:
                    is_main = True
                chain_item = f"{parent}_{item}"
                if chain_item not in types:
                    types[parent]["children"] += 1
                    parent_children_seq = types[parent]["children"]
                    my_parent_id = types[parent]["id"]
                    my_id = str(str(types[parent]["id"]) + "_" + str(parent_children_seq))
                    if is_main is True:
                        types[chain_item] = dict(id=my_id, name=item, children=0, parent=parent,
                                                 parent_id=my_parent_id, is_main=1, url=url
                                                 )
                    else:
                        types[chain_item] = dict(id=my_id, name=item, children=0, parent=parent, parent_id=my_parent_id)
                parent = chain_item
        with open(f"{self._path_3}/{platform_type}.json", "wb") as fw:
            result = json.dumps(types, ensure_ascii=False, indent=4).encode("utf-8")
            fw.write(result)

    def read_excel_file_by_platform_type(self, path):
        """
        读取信源文件。
        :return:
        """

        file = pandas.ExcelFile(path)
        for sheet_name in file.sheet_names:
            table = file.parse(sheet_name)
            for row in table.itertuples():
                for platform_type in self._known_types:
                    if platform_type in row:
                        yield platform_type, row
                        break
                else:
                    for platform_type in self._other_known_types:
                        if platform_type in row:
                            break
                    else:
                        raise ValueError(f"未知类型，{path}，{row}")

    @staticmethod
    def find_excel_file(path):
        """
        查找信源文件。
        :return:
        """

        for root, dirs, files in os.walk(path):
            for file in files:
                path = f"{root}/{file}"
                if (file.endswith(".xlsx") or file.endswith(".xls")) \
                        and "__MACOSX" not in root and not file.startswith("~$"):
                    # pass
                    # print(f"{path}")
                    yield path
                else:
                    pass
                    # print(f"{path}")

    @staticmethod
    def find_target_files(path, suffix):
        """
        查找文件。
        :return:
        """

        for root, dirs, files in os.walk(path):
            for file in files:
                path = f"{root}/{file}"
                if file.endswith(f".{suffix}"):
                    # pass
                    # print(f"{path}")
                    yield path
                else:
                    pass
                    # print(f"{path}")

    def prepare(self):
        """
        准备数据，将不同平台分组。
        :return:
        """

        platform_type_dict = dict()
        error_paths = dict()
        for path in self.find_excel_file(self._path_1):
            # noinspection PyBroadException
            try:
                for platform_type, row in self.read_excel_file_by_platform_type(path):
                    if platform_type not in platform_type_dict:
                        platform_type_dict[platform_type] = list()
                    platform_type_dict[platform_type].append(list(row))
            except Exception as e:
                if path not in error_paths:
                    error_paths[path] = list()
                error_paths[path].append(str(e))
        for platform_type, rows in platform_type_dict.items():
            df = pandas.DataFrame(rows)
            with pandas.ExcelWriter(f"{self._path_2}/{platform_type}.xlsx") as writer:
                df.to_excel(writer, sheet_name=platform_type)
                writer.save()
        print(json.dumps(error_paths, indent=4, ensure_ascii=False))

    def parse(self):
        """
        解析。
        :return:
        """

        for path in self.find_excel_file(self._path_2):
            res = self.parse_excel_file(path)


if __name__ == '__main__':
    SourceData().parse()
