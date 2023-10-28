# -*- coding:utf-8 -*-
"""
爬虫视图。
# author: BigDataTeam，Trico
# date: 2020/12/10
# update: 2020/12/10
"""

import json
import types
import traceback
from django.http import JsonResponse

import spiders.libs.runner as runner
from api_common_utils.llog import LLog
from api.config import api_log_path, kafka_topics
from api_common_utils.utils import log_request_info
from api_common_utils.kafka.kafka_utils import dc_kafka_producer
from api_common_utils.get_public_params import get_data_plural_singular_map

# 初始化日志对象。
SPIDER_LOG_PATH = f"{api_log_path}/spiders"
SPIDER_TYPES = ["spiders", "wechat", "weibo", "website", "app", "epaper", "forum", "we_media"]
LOGGERS = dict()
for SPIDER_TYPE in SPIDER_TYPES:
    LOGGERS[SPIDER_TYPE] = LLog(SPIDER_TYPE, log_path=SPIDER_LOG_PATH, logger_level="DEBUG").logger


# 复数与单数映射。
PLURAL_SINGULAR_MAP = get_data_plural_singular_map(map_direction="p_s")
# 单数与复数映射。
SINGULAR_PLURAL_MAP = get_data_plural_singular_map(map_direction="s_p")


def se(request):
    """执行爬虫。"""

    logger = LOGGERS["spiders"]
    try:
        # 记录请求体。
        log_request_info(logger, request)
        # 爬虫类别，微信、微博等等。
        spider_type = request.GET.get("spider_type")
        assert spider_type in SPIDER_TYPES, f"参数错误，spider_type：{spider_type}"
        # 采集方式，批采集或是流采集。
        fetch_method = request.GET.get("fetch_method")
        if fetch_method:
            assert fetch_method in ["batch", "yield"], f"参数错误，fetch_method：{fetch_method}"
        else:
            fetch_method = "batch"
        # 任务信息。
        task = json.loads(request.body)
        assert task and isinstance(task, (dict, list, str)), f"参数错误，request.body：{task}"

        # 调用爬虫，获取数据。
        spider_logger = LOGGERS[spider_type]
        spider_runner = runner.SpiderRunner(logger=spider_logger, fetch_method=fetch_method)
        if spider_type == "wechat":
            res = spider_runner.fetch_wechat(task)
        elif spider_type == "weibo":
            res = spider_runner.fetch_weibo(task)
        elif spider_type == "website":
            res = spider_runner.fetch_website(task)
        elif spider_type == "app":
            res = spider_runner.fetch_app(task)
        elif spider_type == "epaper":
            res = spider_runner.fetch_epaper(task)
        elif spider_type == "forum":
            res = spider_runner.fetch_forum(task)
        elif spider_type == "we_media":
            res = spider_runner.fetch_we_media(task)
        else:
            raise ValueError(f"未知参数，spider_type：{spider_type}")

        # 整合结果。
        response = dict(code=1, msg="ok")
        count = dict()
        # 结果转存目标。
        result_target = request.GET.get("result_target")
        if result_target:
            if result_target == "kafka":
                # 存储至Kafka。
                topic = kafka_topics["origin"]
                producer = dc_kafka_producer()
                if isinstance(res, dict):
                    # 结果验证。
                    if res.get("code") != 1:
                        raise ValueError(f"采集失败，{res.get('msg')}")
                    res_data = res.get("data", dict())
                    if res_data:
                        for i_name, i_data in res_data.items():
                            try:
                                # 单复数转换。
                                if i_name in PLURAL_SINGULAR_MAP:
                                    i_name = PLURAL_SINGULAR_MAP[i_name]
                                elif i_name in SINGULAR_PLURAL_MAP:
                                    pass
                                else:
                                    spider_logger.warning(f"不熟悉的结构名称：{i_name}")
                                    continue
                                if i_name not in count:
                                    count[i_name] = 0
                                # 将批数据梳理为流数据。
                                if isinstance(i_data, (list, tuple)):
                                    for i_data_child in i_data:
                                        msg = dict(code=1, msg="ok", data={i_name: i_data_child})
                                        msg = json.dumps(msg, separators=(",", ":")).encode("utf-8")
                                        # 注意是单个线程对应单个Kafka生产者。
                                        resp = producer.send(topic=topic, value=msg)
                                        if resp.failed():
                                            raise resp.exception
                                        else:
                                            spider_logger.debug(f"{topic}，{i_name}，{len(msg) / 1024:.2f} KB")
                                            count[i_name] += 1
                                elif isinstance(i_data, dict):
                                    msg = json.dumps(res, separators=(",", ":")).encode("utf-8")
                                    # 注意是单个线程对应单个Kafka生产者。
                                    resp = producer.send(topic=topic, value=msg)
                                    if resp.failed():
                                        raise resp.exception
                                    else:
                                        spider_logger.debug(f"{topic}，{i_name}，{len(msg) / 1024:.2f} KB")
                                        count[i_name] += 1
                            except Exception as e:
                                logger.warning(f"{e}\n{traceback.format_exc()}")
                elif isinstance(res, types.GeneratorType):
                    res_generator = res
                    # 遍历生成器可能会出异常，生成器内部应当妥善处理。
                    for msg_single in res_generator:
                        try:
                            if msg_single.get("code", 0) == 1:
                                res_data = msg_single.get("data", dict())
                                if res_data:
                                    for i_name, i_data in res_data.items():
                                        # 单复数转换。
                                        if i_name in PLURAL_SINGULAR_MAP:
                                            i_name = PLURAL_SINGULAR_MAP[i_name]
                                        elif i_name in SINGULAR_PLURAL_MAP:
                                            pass
                                        else:
                                            spider_logger.warning(f"不熟悉的结构名称：{i_name}")
                                            continue
                                        if i_name not in count:
                                            count[i_name] = 0
                                        # 将批数据梳理为流数据。
                                        if isinstance(i_data, (list, tuple)):
                                            for i_data_child in i_data:
                                                msg = dict(code=1, msg="ok", data={i_name: i_data_child})
                                                msg = json.dumps(msg, separators=(",", ":")).encode("utf-8")
                                                # 注意是单个线程对应单个Kafka生产者。
                                                resp = producer.send(topic=topic, value=msg)
                                                if resp.failed():
                                                    raise resp.exception
                                                else:
                                                    spider_logger.debug(f"{topic}，{i_name}，{len(msg) / 1024:.2f} KB")
                                                    count[i_name] += 1
                                        elif isinstance(i_data, dict):
                                            msg = json.dumps(res, separators=(",", ":")).encode("utf-8")
                                            # 注意是单个线程对应单个Kafka生产者。
                                            resp = producer.send(topic=topic, value=msg)
                                            if resp.failed():
                                                raise resp.exception
                                            else:
                                                spider_logger.debug(f"{topic}，{i_name}，{len(msg) / 1024:.2f} KB")
                                                count[i_name] += 1
                        except Exception as e:
                            logger.warning(f"{e}\n{traceback.format_exc()}")
            else:
                # 返给客户端。
                raise ValueError(f"未知参数，result_target：{result_target}")
        response["data"] = dict(count=count)
        return JsonResponse(response)
    except Exception as e:
        logger.error(f"{e}\n{traceback.format_exc()}")
        return JsonResponse(dict(code=0, msg=str(e)))
