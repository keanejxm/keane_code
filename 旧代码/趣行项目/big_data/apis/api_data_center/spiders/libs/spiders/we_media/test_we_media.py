"""

# author: albert
# date: 2021/1/20 10:08
# update: 2021/1/20 10:08
"""
import elasticsearch
from loguru import logger
from api.config import es_config
from spiders.libs.spiders.we_media.we_media_run import WeMediaRun


def save_yeild_es(res):
    es_conn = elasticsearch.Elasticsearch(**es_config)
    if "account" in res:
        forum = res["account"]
        fetch_id = forum.pop("_id")
        fetch_data = forum
        r = es_conn.index(index="dc_accounts", id=fetch_id, doc_type="_doc", body=fetch_data)
        logger.debug(f'{forum["name"]}: {r}')
    else:
        detail = res["works"]
        _id = detail.pop("_id")
        detail_fetch_data = detail
        r = es_conn.index(index="dc_works", id=_id, doc_type="_doc", body=detail_fetch_data)
        logger.debug(r)


def get_from_platfrom_name(name):
    es_hosts = [dict(
        host="192.168.16.21",
        port=9200,
    )]
    es_conn = elasticsearch.Elasticsearch(hosts=es_hosts)
    body = {
        "size":99,
        "query": {"bool": {"must": [{"term": {"platformName": {"value": name}}}]}
      }
    }
    res = es_conn.search(index="dc_accounts", doc_type="_doc", body=body)
    result = []
    for r in res["hits"]["hits"]:
        data = r["_source"]
        data["_id"] = r["_id"]
        result.append(data)
    return result


def run_platfrom_name(name):
    task_list = get_from_platfrom_name(name=name)
    for task in task_list:
        res = WeMediaRun(logger).fetch_yield(task)
        for r in res:
            if r["code"] == 1:
                save_yeild_es(r["data"])
            print(r)


def run_account_name(name, weMediaName):
    es_hosts = [dict(
        host="192.168.16.21",
        port=9200,
    )]
    es_conn = elasticsearch.Elasticsearch(hosts=es_hosts)
    body = {
        "query": {
            "bool": {
                "must": [
                    {"term": {
                        "name": {
                            "value": name
                        }
                    }},
                    {"term": {
                        "weMediaName": {
                            "value": weMediaName
                        }
                    }
                    }
                ]
            }
        }
    }
    res = es_conn.search(index="dc_accounts", doc_type="_doc", body=body)
    res = res["hits"]["hits"][0]
    data = res["_source"]
    data["_id"] = res["_id"]
    res = WeMediaRun(logger).fetch_yield(data)
    for r in res:
        if r["code"] == 1:
            save_yeild_es(r["data"])
        print(r)
    logger.debug(res)


if __name__ == '__main__':
    # name = "瞭望智库"
    # weMediaName = "澎湃号"

    name = "河北日报"
    weMediaName = "人民号"
    run_account_name(name, weMediaName)

    # run_platfrom_name('冀云APP')
    # run_platfrom_name('人民日报APP')
