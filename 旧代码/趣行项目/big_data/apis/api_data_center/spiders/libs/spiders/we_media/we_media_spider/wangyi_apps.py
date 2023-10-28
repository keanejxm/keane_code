# -*- coding:utf-8 -*-

"""
# author: Chris
# date: 2020/11/24
# update: 2020/11/24
# 网易号任意搜索并采集账户、作品信息
"""
import hashlib
import time
import json
import requests
import traceback
from lxml import etree

from spiders.libs.spiders.we_media.we_media_utils import DEFAULT_WE_MEDIA_USER_INFO_FIELDS, \
    DEFAULT_WE_MEDIA_USER_WORKS_FIELDS


class WangYiAppPcSearch:

    def __init__(self):
        self._session = requests.Session()
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
        }

    def app_search(self, kw):
        url = f"https://dy.163.com/v2/media/search?word={kw}"
        r = self._session.get(url, headers=self._headers)
        if f"<em>查找结果：</em>没有找到“{kw}”相关的订阅栏目。</p>" in r.text:
            return list()
        tree = etree.HTML(r.text)
        result_list = list()
        li_tags = tree.xpath("//ul[@class='column_list clearfix']/li")
        if len(li_tags) > 0:
            for li_tag in li_tags:
                try:
                    if str(li_tag.xpath("div[@class='des']/h3/a/text()")[0]) == kw:
                        result_list.append(str(li_tag.xpath("a[2]/@data")[0]))
                        break
                    else:
                        if li_tag == li_tags[-1]:
                            print("未找到目标，但添加了第一个")
                            result_list.append(str(li_tags[0].xpath("a[2]/@data")[0]))
                except Exception as e:
                    print(e)
        return result_list


class WangYiAccountsAndWorks:

    def __init__(self, logger):
        self.logger = logger
        self._session = requests.Session()
        self._headers = {
            # "User-Agent": "NewsApp/66.1 Android/5.1 (OPPO/OPPO A37m)",
            "User-Agent": "NewsApp/74.1 Android/5.1.1 (HUAWEI/VOG-AL10)",
            # "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; VOG-AL10 Build/HUAWEIVOG-AL10; wv) AppleWebKit/537.36 "
            #               "(KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36",
            # "Host": "nine.ifeng.com",
        }

    @staticmethod
    def md5(unicode_str, charset="UTF-8"):
        """
        字符串转md5格式。
        :return:
        """
        _md5 = hashlib.md5()
        _md5.update(unicode_str.encode(charset))
        return _md5.hexdigest()

    def _fetch_works(self, uid):
        nt = int(time.time()*1000)
        data = {
            "tid": uid,
            "type": "all",
            "offset": 0,
            "size": 20,
            "devId": "Cx12KTE2uYf3EqgHD/AYhw==",
            "devIdOD": "Cx12KTE2uYf3EqgHD/AYhw==",
            "encryption": 1,
            # "version": "74.1",
            # "net": "wifi",
            # "canal": "QQ_news_CPD1",
            # "lat": "WjcNwnRe/v/deTnO5VRsQ6hnYB+xK6YGLcdcZR+srK8=",
            # "lon": "C9OWReN7VsjKaVK+53fsNnjwStHTbMnr8pc6fFfTjog=",
            # "ts": nt,
            # "sign": "miSt0j6aE0cD462hWROCEAOf0GIB3cWkw+3lBnrOd0B48ErR02zJ6/KXOnxX046I",
            # "mac": "lBuXNCfDFEhpSLkTMMnCXQvVdjgSXYDtwEDZ03eH1l8=",
        }
        url = f"https://v6-gw.m.163.com/nc/api/v2/wangyihao/list"
        resp = self._session.get(url, headers=self._headers, params=data)
        res = json.loads(resp.text)
        return res

    def _fetch_article(self, uid):
        # https://v6-gw.m.163.com/nc/api/v1/feed/dynamic/relatedVideoContent?vid=VIQUH9FMC&recid=&withOriginVideo=true&skipType=video&tid=T1588042742858
        url = "https://gw.m.163.com/nc-omad/api/v1/article/preload/{}/full".format(uid)
        resp = self._session.get(url, headers=self._headers)
        res = json.loads(resp.text)
        return res

    def _fetch_article_num(self, uid):
        url = f"https://v6-gentie.ws.126.net/batapi/v1/products/a2869674571f77b5a0867c3d71db5856/" \
              f"thread/app/summary/{uid}?ibc=newsappandriod"
        resp = self._session.get(url, headers=self._headers)
        res = json.loads(resp.content)
        comment_num = int(res["cmtCount"])
        like_num = int(res["threadWeightVote"])
        return comment_num, like_num

    def fetch_all(self, uid):
        resp = self._fetch_works(uid)
        # https://c.m.163.com/news/sub/T1374537989920.html  账号地址

        now = int(time.time() * 1000)
        platformID = "fecc51098acee38b7b5b86ac27d9ca93"
        platformName = "网易号手机客户端"
        account_data = dict(**DEFAULT_WE_MEDIA_USER_INFO_FIELDS)

        account_data["_id"] = self.md5(platformID + str(resp["data"]["subscribe_info"]["ename"]))
        account_data["platformAccountID"] = str(resp["data"]["subscribe_info"]["ename"])
        account_data["name"] = resp["data"]["subscribe_info"]["tname"]
        account_data["avatar"] = resp["data"]["subscribe_info"]["topic_icons"]
        account_data["url"] = f"https://c.m.163.com/news/sub/{uid}.html"
        account_data["platformID"] = platformID
        account_data["platformName"] = platformName
        account_data["weMediaName"] = "网易号"
        account_data["createTime"] = now
        account_data["updateTime"] = now

        nums = resp["data"]["subscribe_info"]["subnum"]
        if "万" in nums:
            account_data["platformFansNum"] = int(float(nums.strip("万")) * 10000)
        else:
            account_data["platformFansNum"] = int(nums)

        res = []
        for info in resp["data"]["tab_list"]:
            try:
                doc_id = info["docid"]
                works_fields = dict(**DEFAULT_WE_MEDIA_USER_WORKS_FIELDS)
                works_fields["_id"] = self.md5(platformID + str(doc_id))
                works_fields["accountID"] = self.md5(platformID + str(resp["data"]["subscribe_info"]["ename"]))
                works_fields["accountName"] = account_data["name"]
                works_fields["platformWorksID"] = doc_id
                works_fields["platformID"] = platformID
                works_fields["platformName"] = platformName

                # article_data["url"] = article["share_url"]
                # article_data["authors"] = [article["copyfrom"]]
                works_fields["title"] = info["title"]
                # article_data["titleWordsNum"] = len(article["title"])
                # article_data["html"] = detail_content.text
                # content = text_remover_html_tag(detail_content_data["frontend"]["contents"])
                # article_data["content"] = content
                # article_data["contentWordsNum"] = len(content)
                # article_data["digest"] = content[:200]
                # article_data["images"] = detail_content_data["frontend"]['image']
                # article_data["covers"] = cover
                # article_data["videos"] = []
                # article_data["readNum"] = self.parser_num(article["read_count"])
                # article_data["likeNum"] = self.parser_num(article["likes_count"])
                works_fields["commentNum"] = int(info["replyCount"])
                # article_data["forwardNum"] = self.parser_num(article["share_count"])
                # article_data["updateParams"] = json.dumps({"article_id": str(article["id"]), "type": str(article["type"])})
                # article_data["contentType"] = 1
                # if article_data["images"]:
                #     article_data["contentType"] = 2
                # if article_data["videos"]:
                #     article_data["contentType"] = 3
                works_fields["createTime"] = now
                works_fields["updateTime"] = now

                pub_time = int(time.mktime(time.strptime(info["ptime"], "%Y-%m-%d %H:%M:%S")))
                works_fields["pubTime"] = pub_time * 1000
                # works_fields["commentNum"] = info["replyCount"]
                # works_fields["likeNum"] = info["votecount"]
                # 调整covers来源，就是单纯从app上看到文章时的情况
                if info["imgsrc"]:
                    works_fields["covers"] = [info["imgsrc"]]
                # 以下covers作为判断文章类型依据
                covers = []
                # 获取文章详情
                if "_" not in doc_id:      # 表示图文
                    ret = self._fetch_article(doc_id)
                    cn, ln = self._fetch_article_num(doc_id)        # 评论数与点赞数
                    works_fields["commentNum"] = cn
                    works_fields["likeNum"] = ln
                    works_fields["wangYiJoinNum"] = cn
                    works_fields["platformWorksID"] = doc_id
                    works_fields["url"] = ret["data"][doc_id]["shareLink"]
                    content = ret["data"][doc_id]["body"]
                    if ret["data"][doc_id]["img"]:
                        # 以下covers作为判断文章类型依据
                        covers = [i["src"] for i in ret["data"][doc_id]["img"]]
                        for i in ret["data"][doc_id]["img"]:
                            content = content.replace(i["ref"], f"<img src='{i['src']}'>")
                    if "video" in ret["data"][doc_id].keys():
                        img_url = [i["cover"] for i in ret["data"][doc_id]["video"]]
                        try:
                            vid_url = [i["url_mp4"] for i in ret["data"][doc_id]["video"]]
                        except:
                            vid_url = [i["mp4_url"] for i in ret["data"][doc_id]["video"]]
                        for i in range(len(ret["data"][doc_id]["video"])):
                            video = f"<div><video src=\"{vid_url[i]}\" poster=\"{img_url[i]}\" " \
                                     f"controls=\"controls\"></video></div>"
                            content = content.replace(ret["data"][doc_id]["video"][i]["ref"], video)
                        works_fields["videos"] = vid_url
                    works_fields["updateParams"] = json.dumps({"doc_id": doc_id}, ensure_ascii=False)
                else:       # 表示视频  f'https://c.m.163.com/news/v/{wid}.html?spss=newsapp'
                    works_fields["platformWorksID"] = info["videoinfo"]["vid"]
                    works_fields["updateParams"] = json.dumps({"doc_id": info["videoinfo"]["vid"],
                                                               "uid": account_data["platformAccountID"]}, ensure_ascii=False)
                    vid_url = info["videoinfo"]["mp4_url"]
                    img_url = info["videoinfo"]["cover"]
                    works_fields["covers"] = [img_url]
                    works_fields["videos"] = [vid_url]
                    content = f"<div><video src=\"{vid_url}\" poster=\"{img_url}\" controls=\"controls\"></video></div>"
                    works_fields["url"] = f"https://c.m.163.com/news/v/{works_fields['mediaWorkId']}.html?spss=newsapp"
                    works_fields["commentNum"] = info["replyCount"]     # 评论数
                    works_fields["likeNum"] = info["upTimes"]           # 点赞数
                works_fields["content"] = content
                if len(works_fields["videos"]) != 0:
                    works_fields["contentType"] = 3
                elif len(works_fields["videos"]) == 0 and len(covers) != 0:
                    works_fields["contentType"] = 2
                res.append(works_fields)
            except Exception as e:
                print(f"{e}.\n{traceback.format_exc()}")
                continue
        return dict(
            code=1,
            msg="success",
            total=len(res),
            data=dict(
                account=account_data,
                works=res
            )
        )

    def run(self, uid):
        return self.fetch_all(uid)

    def fetch(self, task):
        try:
            res = self.run(task["platformAccountID"])
            return res
        except Exception as e:
            self.logger.warning(f"{e}\n{traceback.format_exc()}")
            return dict(code=0, msg=str(e))


if __name__ == '__main__':
    from loguru import logger
    # keyword = "河北新闻网"
    keyword = "流行唯一"
    uu = WangYiAppPcSearch().app_search(keyword)
    if uu:
        result = WangYiAccountsAndWorks(logger).run(uu[0])
        # print(result)
        with open(keyword + "result.json", "w", encoding="utf8") as f:
            f.write(json.dumps(result, indent=4, ensure_ascii=False))


