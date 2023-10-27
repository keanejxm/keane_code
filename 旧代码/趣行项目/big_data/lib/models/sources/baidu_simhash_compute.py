# -*- coding: utf-8 -*-#

"""
# 计算作品的simhash值并更新
# author: Chris
# date: 2021/1/12
# update: 2021/1/12
"""


import json
import traceback
import requests
import elasticsearch
from bs4 import BeautifulSoup


class EsDataCompute:

    def __init__(self, logger):
        self._logger = logger
        self.target_index = "dc_works"
        self.simhash_url = "http://180.76.96.208:16301/dc/flow_compute/common/get_simhash_value/"
        self._es_conn = elasticsearch.Elasticsearch([{"host": "180.76.161.67", "port": 9200}])

    def data_from_es(self):
        result = list()
        must_list = [
            {"range": {"pubTime": {
                "gte": 1609948800000,   # 1月7日
                # "lte": end_time
            }}}]
        body = {
            "size": 9999,
            "_source": ["simhash", "content", "title", "contentType"],
            "query": {"bool": {"must": must_list}},
        }
        res1 = self._es_conn.search(index=self.target_index, request_timeout=3600, body=body)
        logger.debug(res1["hits"]["total"])
        if res1["hits"]["total"] > 0:
            for work in res1["hits"]["hits"]:
                item = work["_source"]
                item["_id"] = work["_id"]
                result.append(item)
        return result

    def update_simhash_to_es(self, source_detail):
        filed_id = source_detail.pop("_id")
        fileds = {"doc": {"simhash": source_detail["simhash"]}}
        res = self._es_conn.update(index=self.target_index, doc_type="_doc", id=filed_id, body=fileds)
        logger.info(f"{filed_id}，{res['result']}")
        return res

    def simhash_compute(self, source_detail):
        content = source_detail["content"]
        soup = BeautifulSoup(content, "html.parser")
        content = soup.get_text()
        data = {"content": content, "need_cleaning": "need"}
        try:
            resp = requests.post(self.simhash_url, json=data)
            logger.info(resp.text)
            res = json.loads(resp.text)
            simhash = res["data"]
        except Exception as e:
            self._logger.warning("报错之处在于：{}.\n{}".format(e, traceback.format_exc()))
            simhash = ""
        source_detail["simhash"] = simhash
        return source_detail

    def run(self):
        result = self.data_from_es()
        for item in result:
            # 进行simhash计算条件是字段为空，作品类型不是纯长、短视频、画廊、音频
            try:
                if not item["simhash"] and int(item["contentType"]) not in [4, 5, 6, 7]:
                    source_detail = self.simhash_compute(item)
                    if source_detail["simhash"]:
                        self.update_simhash_to_es(source_detail)
            except Exception as e:
                logger.warning("报错之处在于：{}.\n{}".format(e, traceback.format_exc()))
                continue


if __name__ == '__main__':
    from lib.common_utils.llog import LLog
    logger = LLog("test", only_console=True).logger
    # EsDataCompute().data_from_es()
    sod = {
          "content": """<p><span class="bjh-p">2021年1月3日0—24时，南宫市新增新冠肺炎确诊病例2例和无症状感染者1例。目前，对所有追踪到的密切接触者已全部采取隔离医学观察，各项疫情防控措施有序进行。现将其行程轨迹公布如下：</span></p><p><span class="bjh-p"><span class="bjh-strong">确诊病例一：</span>男，34岁，南宫市天一和院小区居民。2020年12月19日至24日单位上班无外出。25日携家人自驾到省儿童医院看病。28日至31日正常上班，期间在南宫市天一酒店参加午宴。2021年1月1日到南宫市人民医院检测核酸，2日20:00样本呈阳性，随即被采取集中隔离观察措施。3日诊断为确诊病例。（普通型）</span></p><p><span class="bjh-p"><span class="bjh-strong">确诊病例二：</span>男，30岁，南宫市天地名城小区居民，为确诊病例一的弟弟。2020年12月18日核酸检测为阴性。21日自驾到邢台东站，乘坐G655次列车2车厢到洛阳入住友谊宾馆。22日到华阳宾馆参加农机展销会。23日乘坐G1712次列车3车厢到邢台东站，自驾回家。24日自驾到省儿童医院。25日至27日，先后在南宫市万和超市、得力文具、旭日通信、新胜利超市购物，寺庄羊汤就餐。28日在天一快捷酒店参加推销活动。29日至2021年1月1日，曾到过天幔理发馆、万和超市。2日到河北省眼科医院就诊，乘坐G1560次列车3车厢到石家庄就餐，乘坐G491次列车1车厢返回邢台。20:30被采取集中隔离观察措施。3日诊断为确诊病例。（轻型）</span></p><p><span class="bjh-p"><span class="bjh-strong">无症状感染病例一：</span>女，31岁，南宫市天一和院小区居民，为确诊病例一的妻子。2020年12月17日至24日，每日接送儿子上下学，曾到过蚂蚁汽车装饰店、华座便利店、晓田祥快餐。25日7时同家人自驾到省儿童医院看病。26日至29日，每日接送儿子上下学，曾到棠熙便利店购物。30日，到省儿童医院看病。31日至2021年1月2日，每天接送孩子上下学，期间到过杜妈妈棉衣店、至诚装饰。与确诊病例一同一时间被采取集中隔离观察措施。3日被确定为无症状感染者。</span></p><p><span class="bjh-p">在此提醒广大市民，如果在相同时间、地点有以上共同活动轨迹或近期接触过上述地区相关人员的，请第一时间向居住地乡镇、街道报告，配合做好防控管理和核酸检测。</span></p><p><span class="bjh-p">（南宫发布）</span></p>"""
}
    sod1 = EsDataCompute(logger).simhash_compute(sod)
    # EsDataCompute(logger).update_simhash_to_es(sod1)
    # EsDataCompute(logger).run()
