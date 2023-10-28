# -*- coding:utf-8 -*-
"""

# author: albert
# date: 2021/1/5
# update: 2021/1/5
"""
from spiders.libs.spiders.forum.parse import *
import copy

class ForumRun:

    def __init__(self, logger):
        self.logger = logger

    def carry_out_a_task(self, task):
        try:
            task_url = task["url"]
            _json = False
            if task["levelNumber"] == 0 and task["platformName"] == "百度贴吧":
                _json = True
            parse_model = {
                # 大分类
                "1": dc_forum_from_es,
                # 小分类
                "2": dc_forum,
                # 贴吧
                "3": dc_forum_details,
                # 知乎贴吧
                "3_1": dc_zhifu_forum_details,
                # 贴吧热榜
                "0": dc_hot_forum,
                # 知乎热榜
                "0_1": dc_zhihu_hot_forum,
                # 热榜话题
                "4": dc_forum_hot_details,
                # 知乎热榜话题
                "4_1": dc_zhihu_forum_hot_details,
            }
            # 判断任务 根据任务分给对应的解析器
            if task["platformName"] == "知乎":
                if task["levelNumber"] == 0:
                    headers = {
                        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36"
                    }
                    result = downloader(task_url, header=headers)
                    parse_result = parse_model['0_1'](task, result)
                elif task["levelNumber"] == 3:
                    result = downloader(task_url, json=_json)
                    parse_result = parse_model['3_1'](task, result)
                elif task["levelNumber"] == 4:
                    result = downloader(task_url, json=_json)
                    parse_result = parse_model['4_1'](task, result)
                else:
                    parse_result = None
            else:
                result = downloader(task_url, json=_json)
                parse_result = parse_model[str(task["levelNumber"])](task, result)

            if "dc_forum" in parse_result:
                return parse_result, False
            else:
                return parse_result, True
        except Exception as e:
            logger.error(f'Error Msg: {e}\n{traceback.format_exc()}')
            logger.error(f'Error task: {task}')
            return {"dc_forum_details": [], "dc_forum": []}, True

    def scheduler(self, task):
        res, status = self.carry_out_a_task(task)
        _dc_forums = []
        _dc_forum_details = []
        task_list = []
        if status:
            _dc_forum_details.extend(res["dc_forum_details"])
            data = {
                "code": 1,
                "msg": "success",
                "data": {
                    "forums": _dc_forums,
                    "forumDetails": _dc_forum_details,
                }
            }
            return data
        else:
            task_list.extend(res["dc_forum"])
            _dc_forums.extend(task_list)
            for new_task in task_list:
                res, status = self.carry_out_a_task(new_task)
                _dc_forum_details.extend(res["dc_forum_details"])
                if status:
                    _dc_forum_details.extend(res["dc_forum_details"])
                else:
                    task_list.extend(res["dc_forum"])
                    _dc_forums.extend(task_list)
            data = {
                "code": 1,
                "msg": "success",
                "data": {
                    "forums": _dc_forums,
                    "forumDetails": _dc_forum_details,
                }
            }
            return data

    def scheduler_yield(self, task):
        res, status = self.carry_out_a_task(task)
        task_list = []
        if res.get("dc_forum"):
            task_list = copy.deepcopy(res["dc_forum"])
        if status:
            for fd in res["dc_forum_details"]:
                yield dict(code=1, msg="success", data={"forumDetail": fd})
        else:
            for f in res["dc_forum"]:
                yield dict(code=1, msg="success", data={"forum": f})
            del res
            while len(task_list) > 0:
                task = task_list[0]
                new_res, new_status = self.carry_out_a_task(task)
                task_list.pop(0)
                if new_status:
                    for fd in new_res["dc_forum_details"]:
                        yield dict(code=1, msg="success", data={"forumDetail": fd})
                else:
                    new_task_list = new_res["dc_forum"]
                    task_list.extend(new_task_list)
                    for f in new_res["dc_forum"]:
                        yield dict(code=1, msg="success", data={"forum": f})

    def fetch_batch(self, task):
        self.logger.debug(f'论坛爬虫任务{task}')
        return self.scheduler(task)

    def fetch_yield(self, task):
        """
        :param task: 微信任务 - 从es中查询出来的任务 - 一个字典 需要包含_id
        :return:
        """
        self.logger.debug(f'论坛爬虫任务{task}')
        return self.scheduler_yield(task)


if __name__ == '__main__':
    pass

