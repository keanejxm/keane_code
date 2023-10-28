# -*- coding:utf-8 -*-
"""
测试。
# author: Trico
# date: 2021/1/15
# update: 2021/1/15
"""

from common_utils.llog import LLog


def test():
    # 测试。

    from scripts.kafka_listener.a2_save_to_es import KafkaListenerA2FromFlowComputedToES
    logger = LLog(f"test", only_console=True, logger_level="DEBUG").logger
    data = dict(
        _id="bbc3f720c9317949530f84a71397e6c8",
        extendData="""{"latestPaperTime": 1611158400000, "latestPaperFrontPageImage": "http://paper.people.com.cn/rmrb/images/2021-01/21/01/rmrb2021012101_b.jpg"}"""
    )
    KafkaListenerA2FromFlowComputedToES(logger).deal_with_platforms(data)


if __name__ == "__main__":
    test()
