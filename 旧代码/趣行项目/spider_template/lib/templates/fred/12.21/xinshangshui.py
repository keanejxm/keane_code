# -*- encoding:utf-8 -*-
"""
@功能:新湖南解析模板
@AUTHOR：Keane
@文件名：xinhunan.py
@时间：2020/12/17  17:33
"""

import json
import logging
import requests
from lxml import html
from html.parser import HTMLParser
from App.appspider_m import Appspider
from App.initclass import InitClass


class XinHuNan(Appspider):
    #请求频道
    @staticmethod
    def get_app_params():
        url = "https://app.shangshuitv.com/mag/index/v2/index/pages"
        headers = {
            "method": "GET",
            "path": "/mag/index/v2/index/pages",
            "authority": "app.shangshuitv.com",
            "scheme": "https",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 MAGAPPX|4.6.2-3.1.0-13|Android 6.0.1 Android MuMu|shangshuitv|X9IAiiXGUg4DAGSKJgN0nZPA|aa57db95f7dcaa53adbb476e07a1d1e2|8f4fd4cada121910a2b1d135ccaee772",
            "accept-encoding": "gzip",
        }
        data = {}
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
        yield app_params

    #解析频道
    @staticmethod
    def analyze_channel(channelsres):
        channelsparams = []
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent = 4, ensure_ascii = False))

        # print("channelslists==",channelslists)
        index_fragment = channelslists["index_fragment"]
        channels_list = json.loads(index_fragment)
        # #print("channels_list==",channels_list)

        # channels_list = [{
        #     'name': '首页推荐',
        #     'id': '3',
        #     'uniqid': '5c86184da819f',
        # }]

        # channels_list = [{
        #     'name': '中心工作',
        #     'id': '6',
        #     'uniqid': '5cabfb4a5b5d3',
        # }]

        for channel in channels_list:
            channelname = channel["name"]
            channelid = channel["id"]
            uniqid = channel["uniqid"]

            # 请求频道的cat_id
            url = "https://app.shangshuitv.com/mag/info/v1/channel/channelConfigById?channel_id=" + channelid
            headers = {
                "path": url,
                "authority": "app.shangshuitv.com",
                "scheme": "https",
                "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 MAGAPPX|4.6.2-3.1.0-13|Android 6.0.1 Android MuMu|shangshuitv|X9IAiiXGUg4DAGSKJgN0nZPA|aa57db95f7dcaa53adbb476e07a1d1e2|8f4fd4cada121910a2b1d135ccaee772",
                "accept-encoding": "gzip",
                "cookie": "PHPSESSID=s9tt1iu4q9st62vaj3ugpaand0"
            }
            data = {}
            res = requests.get(url, headers=headers, data=data).text
            configinfo = json.loads(json.dumps(json.loads(res, strict=False), indent=4,ensure_ascii=False))
            cat_id = configinfo["data"]["info_config"][0]["cat_id"]


            #banner
            if channelname == "首页推荐":
                #banner
                place = configinfo["data"]["operative_config"][0]["place"]
                channelparam = InitClass().channel_fields(place, "首页banner")
                channelsparams.append(channelparam)

                # 请求二级频道
                fixopconfig = configinfo["data"]["operative_config"][2]

                # 二级频道列表
                topicitems = fixopconfig["items"]
                for topic in topicitems:
                    # topic["picId"]
                    # print("topic=",topic)
                    topiclink = topic["link"]
                    topictitle = topic["title"]

                    if "needlogin=1" in topiclink:
                        print("需要登录，不处理")
                        continue
                    elif "regid=" in topiclink:
                        print("外链，不处理")
                        continue
                    elif "cat_id=" in topiclink:
                        #有不用再次请求
                        cids = topiclink.split("cat_id=")
                        topiccatid = cids[1]

                        subchannelid = channelid + "-" + topiccatid
                        subchannelname = channelname + "-" + topictitle

                        # topiccatid 列表需要id
                        # 工作专题 标记
                        # categoryid 新channelid
                        # categoryname 新 channelname
                        channelparam = InitClass().channel_fields(topiccatid, "首页快捷入口", categoryid=subchannelid,categoryname=subchannelname)
                        channelsparams.append(channelparam)
                    else:
                        #去要请求catid
                        cids = topiclink.split("channel_id=")
                        topicid = cids[1]
                        # 请求专题信息
                        topicurl = "https://app.shangshuitv.com/mag/info/v1/channel/channelConfigById?channel_id=" + str(topicid)
                        topicheaders = {
                            "path": topicurl,
                            "authority": "app.shangshuitv.com",
                            "scheme": "https",
                            "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 MAGAPPX|4.6.2-3.1.0-13|Android 6.0.1 Android MuMu|shangshuitv|X9IAiiXGUg4DAGSKJgN0nZPA|aa57db95f7dcaa53adbb476e07a1d1e2|8f4fd4cada121910a2b1d135ccaee772",
                            "accept-encoding": "gzip",
                            "cookie": "PHPSESSID=s9tt1iu4q9st62vaj3ugpaand0"
                        }
                        topicdata = {}
                        topicres = requests.get(topicurl, headers=topicheaders, data=topicdata).text
                        topicinfo = json.loads(json.dumps(json.loads(topicres, strict=False), indent=4,ensure_ascii=False))

                        topiccatid = topicinfo["data"]["info_config"][0]["cat_id"]
                        catname = topicinfo["data"]["info_config"][0]["cat_name"]

                        subchannelid = channelid + "-" + str(topiccatid)
                        subchannelname = channelname + "-" + catname

                        #topiccatid 列表需要id
                        #工作专题 标记
                        #categoryid 新channelid
                        #categoryname 新 channelname
                        channelparam = InitClass().channel_fields(topiccatid, "首页快捷入口",categoryid=subchannelid, categoryname=subchannelname)
                        channelsparams.append(channelparam)


            elif channelname == "中心工作":

                #请求二级频道
                fixopconfig = configinfo["data"]["operative_config"][1]

                #二级频道列表
                topicitems = fixopconfig["items"]

                for topic in topicitems:
                    # topic["picId"]
                    # print("topic=",topic)
                    topiclink = topic["link"]
                    coverurl = topic["pic"]

                    if "cat_id=" in topiclink:
                        #有不用再次请求
                        cids = topiclink.split("cat_id=")
                        topiccatid = cids[1]

                        catname = "百城提质"

                        subchannelid = channelid + "-" + topiccatid
                        subchannelname = channelname + "-" + catname

                        # topiccatid 列表需要id
                        # 工作专题 标记
                        # categoryid 新channelid
                        # categoryname 新 channelname
                        channelparam = InitClass().channel_fields(topiccatid, "工作专题", categoryid=subchannelid,categoryname=subchannelname)
                        channelsparams.append(channelparam)
                    else:
                        #去要请求catid
                        cids = topiclink.split("channel_id=")
                        topicid = cids[1]
                        # 请求专题信息
                        topicurl = "https://app.shangshuitv.com/mag/info/v1/channel/channelConfigById?channel_id=" + str(topicid)
                        topicheaders = {
                            "path": topicurl,
                            "authority": "app.shangshuitv.com",
                            "scheme": "https",
                            "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 MAGAPPX|4.6.2-3.1.0-13|Android 6.0.1 Android MuMu|shangshuitv|X9IAiiXGUg4DAGSKJgN0nZPA|aa57db95f7dcaa53adbb476e07a1d1e2|8f4fd4cada121910a2b1d135ccaee772",
                            "accept-encoding": "gzip",
                            "cookie": "PHPSESSID=s9tt1iu4q9st62vaj3ugpaand0"
                        }
                        topicdata = {}
                        topicres = requests.get(topicurl, headers=topicheaders, data=topicdata).text
                        topicinfo = json.loads(json.dumps(json.loads(topicres, strict=False), indent=4,ensure_ascii=False))

                        topiccatid = topicinfo["data"]["info_config"][0]["cat_id"]
                        catname = topicinfo["data"]["info_config"][0]["cat_name"]

                        subchannelid = channelid + "-" + str(topiccatid)
                        subchannelname = channelname + "-" + catname

                        #topiccatid 列表需要id
                        #工作专题 标记
                        #categoryid 新channelid
                        #categoryname 新 channelname
                        channelparam = InitClass().channel_fields(topiccatid, "工作专题",categoryid=subchannelid, categoryname=subchannelname)
                        channelsparams.append(channelparam)

            elif channelname == "商水新闻":
                column_id = configinfo["data"]["operative_config"][0]["column_id"]
                channelid = column_id
                channelname = configinfo["data"]["operative_config"][0]["title"]

            channelparam = InitClass().channel_fields(channelid,channelname,categoryid=uniqid,categoryname=cat_id)
            channelsparams.append(channelparam)

        yield channelsparams

    #请求各频道列表
    @staticmethod
    def getarticlelistparams(channelsparams):
        articlelistsparams = []

        tab = 0
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = ""#channel.get("channeltype")  # 此处没有若有可加上，其他一样
            uniqid = channel.get("categoryid")
            cat_id = channel.get("categoryname")

            method = 'get'
            if channelname == "首页banner":
                url = "https://app.shangshuitv.com/mag/operative/v1/ad/listNotEndByPlace?"
                headers = {
                    "method": "GET",
                    "authority": "app.shangshuitv.com",
                    "scheme": "https",
                    "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 MAGAPPX|4.6.2-3.1.0-13|Android 6.0.1 Android MuMu|shangshuitv|X9IAiiXGUg4DAGSKJgN0nZPA|aa57db95f7dcaa53adbb476e07a1d1e2|8f4fd4cada121910a2b1d135ccaee772",
                    "accept-encoding": "gzip",
                    "cookie": "PHPSESSID=s9tt1iu4q9st62vaj3ugpaand0"
                }
                data = {
                    "place": channelid
                }
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                           channelid=channelid, data=data,
                                                                           channeltype=channeltype,banners=1)
                articlelistsparams.append(articlelist_param)
                continue

            elif channelname == "商水新闻联播":
                url = "https://app.shangshuitv.com/mag/livevideo/v1/Video/columnVideoList"
                headers = {
                    "method": "GET",
                    "authority": "app.shangshuitv.com",
                    "scheme": "https",
                    "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 MAGAPPX|4.6.2-3.1.0-13|Android 6.0.1 Android MuMu|shangshuitv|X9IAiiXGUg4DAGSKJgN0nZPA|aa57db95f7dcaa53adbb476e07a1d1e2|8f4fd4cada121910a2b1d135ccaee772",
                    "accept-encoding": "gzip",
                    "cookie": "PHPSESSID=s9tt1iu4q9st62vaj3ugpaand0"
                }
                data = {
                    "column_id":channelid,
                    "p": 1,
                }
                tab += 1
            elif channelname == "工作专题" or channelname == "首页快捷入口":

                url = "https://app.shangshuitv.com/mag/info/v2/info/infoListByCatId?"
                data = {
                    "cat_id": channelid,
                    "p": 1,
                }
                headers = {
                    "method": "GET",
                    "authority": "app.shangshuitv.com",
                    "scheme": "https",
                    "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 MAGAPPX|4.6.2-3.1.0-13|Android 6.0.1 Android MuMu|shangshuitv|X9IAiiXGUg4DAGSKJgN0nZPA|aa57db95f7dcaa53adbb476e07a1d1e2|8f4fd4cada121910a2b1d135ccaee772",
                    "accept-encoding": "gzip",
                    "cookie": "PHPSESSID=s9tt1iu4q9st62vaj3ugpaand0"
                }

                # categoryid 新channelid
                # categoryname 新 channelname
                subchannelid = channel.get("categoryid")
                subchannelname = channel.get("categoryname")
                articlelist_param = InitClass().articlelists_params_fields(url, headers, method, subchannelname,
                                                                           channelid=subchannelid, data=data,
                                                                           channeltype=channeltype)
                articlelistsparams.append(articlelist_param)
                continue

            else:

                url = "https://app.shangshuitv.com/mag/info/v2/info/infoListByCatId?"
                headers = {
                    "oauth-token": "",
                    "udid": "abeaaf99-9a55-4232-96c7-79ddba532c77",
                    "Host": "cgi.voc.com.cn",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/4.2.2",
                }

                data = {
                    "cat_id": cat_id,
                    "tab": tab,
                    "p": 1,
                    "uniqid": uniqid
                }
                tab += 1
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid = channelid, data = data,
                                                                       channeltype = channeltype)
            articlelistsparams.append(articlelist_param)


        yield articlelistsparams

    #解析各频道列表
    @staticmethod
    def analyze_articlelists(articleslistsres):
        articlesparams = []
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            channel_type = ""#articleslistres.get("channeltype")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent = 4, ensure_ascii = False))
                try:
                    # print("articleslists ==",articleslists)
                    article_list = articleslists["list"]

                    if channelname == "首页banner":
                        channelname = "首页推荐"
                        for banneritem in article_list:
                            # 普通
                            article_fields = InitClass().article_fields()
                            articleparam = InitClass().article_list_fields()

                            # article_id = banneritem["id"]
                            article_title = banneritem["title"]
                            pics_arr = banneritem["pic_arr"]
                            article_covers = list()
                            for pic in pics_arr:
                                picurl = pic["url"]
                                article_covers.append(picurl)
                            article_fields["articlecovers"] = article_covers

                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelType"] = channel_type

                            article_fields["title"] = article_title
                            # article_fields["contentType"] = article_type
                            # article_fields["url"] = share_url
                            # article_fields["pubtime"] = pubtime
                            article_fields["banner"] = 1

                            link = banneritem["link"]
                            if "cat_id=" in link:
                                #专题新闻 其余频道已抓取
                                cids = link.split("cat_id=")
                                cat_id = cids[1]
                                article_id = cat_id
                                article_fields["workerid"] = article_id
                                continue
                            elif "id=" in link:
                                #普通新闻
                                cids = link.split("id=")
                                cat_id = cids[1]
                                article_id = cat_id
                                article_fields["workerid"] = article_id

                                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)

                            else:
                                #外部链接
                                article_fields["url"] = link
                                article_fields["appname"] = "新商水"
                                article_fields["images"] = []
                                article_fields["videos"] = []
                                article_fields["videocover"] = []
                                article_fields["pubtime"] = 0
                                article_fields["createtime"] = 0
                                article_fields["updatetime"] = 0

                                print("外部文章==", json.dumps(article_fields, indent=4, ensure_ascii=False))
                                continue

                    elif channelname == "商水新闻联播":
                        for lianbo in article_list:
                            article_fields = InitClass().article_fields()

                            article_id = lianbo["video_content_id"]
                            article_title = lianbo["title"]
                            videourl = lianbo["video_url"]
                            videocover = lianbo["cover_pic_url"]
                            likenum = lianbo["praise_num"]
                            comnum = lianbo["comment_num"]
                            width = lianbo["cover_pic_width"]
                            height = lianbo["cover_pic_height"]

                            source = lianbo["source"]
                            playnum = lianbo["play_num_"]

                            article_fields["source"] = source
                            article_fields["articlecovers"] = [videocover]
                            article_fields["channelID"] = channelid
                            article_fields["channelname"] = channelname
                            article_fields["channelType"] = channel_type
                            article_fields["workerid"] = article_id
                            article_fields["title"] = article_title
                            article_fields["specialtopic"] = 0
                            article_fields["banner"] = 0
                            article_fields["trannum"] = likenum
                            article_fields["playnum"] = playnum
                            article_fields["commentnum"] = comnum
                            article_fields["width"] = width
                            article_fields["height"] = height
                            article_fields["videocover"] = [videocover]
                            article_fields["videos"] = [videourl]
                            article_fields["images"] = []

                            article_fields["appname"] = "新商水"
                            article_fields["createtime"] = 0
                            article_fields["pubtime"] = 0
                            article_fields["updatetime"] = 0

                            print("新闻联播文章=", json.dumps(article_fields, indent=4, ensure_ascii=False))
                        continue

                    else:

                        for article in article_list:
                            if "_name" in article.keys():
                                #列表内专题
                                # print("列表内专题")

                                topic_fields = InitClass().topic_fields()
                                articleparam = InitClass().article_list_fields()

                                article_title = article["title"]
                                morelink = article["more_link"]
                                ids = morelink.split("subjectId=")
                                subid = ids[1]
                                # print("subid==",subid)

                                #请求专题id
                                tmpurl = "https://app.shangshuitv.com/mag/info/v1/Info/infoSubject?subject_id="+str(subid)
                                #tmpurl = "https://app.shangshuitv.com/mag/info/v1/Info/infoSubject?"
                                tmpheaders = {
                                    "method": "GET",
                                    "authority": "app.shangshuitv.com",
                                    "scheme": "https",
                                    "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 MAGAPPX|4.6.2-3.1.0-13|Android 6.0.1 Android MuMu|shangshuitv|X9IAiiXGUg4DAGSKJgN0nZPA|aa57db95f7dcaa53adbb476e07a1d1e2|8f4fd4cada121910a2b1d135ccaee772",
                                    "accept-encoding": "gzip",
                                    "cookie": "PHPSESSID=s9tt1iu4q9st62vaj3ugpaand0"
                                }
                                tmpdata = {

                                }

                                res = requests.get(tmpurl, headers=tmpheaders,data=tmpdata).text
                                configinfo = json.loads(json.dumps(json.loads(res, strict=False), indent=4,
                                                                   ensure_ascii=False))


                                tpic = configinfo["data"]["pic_url"]
                                des = configinfo["data"]["des"]
                                topicCover = list()
                                topicCover.append(tpic)
                                topic_fields["topicCover"] = topicCover
                                topic_fields["digest"] = des
                                shareurl = configinfo["data"]["sharedata"]["linkurl"]
                                topic_fields["topicUrl"] = shareurl

                                info_cat = configinfo["data"]["info_cat"][0]
                                cat_id = info_cat["id"]
                                article_id = cat_id

                                topic_fields["channelName"] = channelname
                                topic_fields["channelID"] = channelid

                                topic_fields["topicID"] = article_id
                                topic_fields["title"] = article_title

                                topic_fields["topic"] = 1
                                # 将请求文章必需信息存入
                                articleparam["articleField"] = topic_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id
                                articlesparams.append(articleparam)

                            else:

                                #普通
                                article_fields = InitClass().article_fields()
                                articleparam = InitClass().article_list_fields()

                                article_id = article["id"]
                                article_title = article["title"]

                                article_covers = list()
                                try:
                                    pics_arr = article["pics_arr"]
                                    for pic in pics_arr:
                                        picurl = pic["url"]
                                        article_covers.append(picurl)
                                    article_fields["articlecovers"] = article_covers
                                except Exception as e:
                                    print("1张图")
                                    try:
                                        picurl = article["pic_arr"]
                                        article_covers.append(picurl)
                                        article_fields["articlecovers"] = article_covers
                                    except Exception as e:
                                        print("无图")

                                article_fields["channelID"] = channelid
                                article_fields["channelname"] = channelname
                                article_fields["channelType"] = channel_type
                                article_fields["workerid"] = article_id
                                article_fields["title"] = article_title
                                # article_fields["contentType"] = article_type
                                # article_fields["url"] = share_url
                                # article_fields["pubtime"] = pubtime
                                article_fields["banner"] = 0
                                articleparam["articleField"] = article_fields  # 携带文章采集的数据
                                articleparam["articleid"] = article_id

                                articletype = article["type"]
                                #1
                                #4 外部
                                if articletype == 4:
                                    source = article["from"]
                                    article_fields["source"] = source
                                    type_value = article["type_value"]
                                    article_fields["url"] = type_value
                                    article_fields["appname"] = "新商水"
                                    article_fields["images"] = []
                                    article_fields["videos"] = []
                                    article_fields["videocover"] = []
                                    article_fields["pubtime"] = 0
                                    article_fields["createtime"] = 0
                                    article_fields["updatetime"] = 0

                                    print("外部文章==", json.dumps(article_fields, indent=4, ensure_ascii=False))
                                    continue

                                else:
                                    from_read = article["from"]
                                    splist = from_read.split("　")
                                    # print("splist==",splist)
                                    if len(splist) >= 2:
                                        source = splist[0]
                                        readnum = splist[1].replace('阅读', '')
                                        article_fields["source"] = source
                                        article_fields["readnum"] = readnum
                                    articlesparams.append(articleparam)

                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")
        yield articlesparams

    #请求详情
    @staticmethod
    def getarticleparams(articles):
        articleparams = []
        for article in articles:
            articleid = article.get("articleid")
            article_field = article.get("articleField")
            topic = article_field.get("topic")

            method = 'get'
            if topic == 1:
                url = "https://app.shangshuitv.com/mag/info/v2/info/infoListByCatId?"
                headers = {
                    "method": "GET",
                    "authority": "app.shangshuitv.com",
                    "scheme": "https",
                    "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 MAGAPPX|4.6.2-3.1.0-13|Android 6.0.1 Android MuMu|shangshuitv|X9IAiiXGUg4DAGSKJgN0nZPA|aa57db95f7dcaa53adbb476e07a1d1e2|8f4fd4cada121910a2b1d135ccaee772",
                    "accept-encoding": "gzip",
                    "cookie": "PHPSESSID=s9tt1iu4q9st62vaj3ugpaand0",
                }
                data = {
                    "cat_id": articleid,
                    "p": 1
                }
            else:
                url = "https://app.shangshuitv.com//mag/info/v1/info/infoView?"
                headers = {
                    "method": "GET",
                    "authority": "app.shangshuitv.com",
                    "scheme": "https",
                    "pragma": "no-cache",
                    "cache-control": "no-cache",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 MAGAPPX|4.6.2-3.1.0-13|Android 6.0.1 Android MuMu|shangshuitv|X9IAiiXGUg4DAGSKJgN0nZPA|aa57db95f7dcaa53adbb476e07a1d1e2|8f4fd4cada121910a2b1d135ccaee772",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "accept-encoding": "gzip, deflate",
                    "accept-language": "zh-CN,en-US;q=0.8",
                    "cookie": "PHPSESSID=ind2qggahnih4pb7uuabq90dv1",
                    "x-requested-with": "com.xinshangshui.app"
                }
                data = {
                    "id":articleid,
                    "mag_hide_progress":1,
                    "themecolor":"D00403"
                }


                openurl = "https://app.shangshuitv.com//mag/info/v1/info/infoView?id="+str(articleid)+"&mag_hide_progress=1&themecolor=D00403"
                article_field["url"] = openurl

            articleparam = InitClass().article_params_fields(url, headers, method, data = data,
                                                             article_field = article_field)
            articleparams.append(articleparam)
        yield articleparams

    #解析详情
    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            topic = fields.get("topic")
            if topic:
                try:
                    content_s = json.loads(
                        json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                    # print("专题二级 ==", content_s)
                    topiclist = content_s["list"]

                    channelid = fields["channelID"]
                    channelname = fields["channelName"]
                    topicid = fields["topicID"]
                    topictitle = fields["title"]

                    articleids = list()
                    totaltopicnum = len(topiclist)
                    fields["articleNum"] = totaltopicnum

                    #请求专题内新闻
                    for article in topiclist:

                        article_fields = InitClass().article_fields()

                        article_id = article["id"]
                        articleids.append(article_id)
                        article_title = article["title"]

                        pics_arr = article["pics_arr"]
                        article_covers = list()
                        for pic in pics_arr:
                            picurl = pic["url"]
                            article_covers.append(picurl)
                        article_fields["articlecovers"] = article_covers

                        from_read = article["from"]
                        splist = from_read.split("　")
                        # print("splist==", splist)
                        if len(splist) >= 2:
                            source = splist[0]
                            readnum = splist[1].replace('阅读', '')
                            article_fields["source"] = source
                            article_fields["readnum"] = readnum

                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = channelname
                        article_fields["channelType"] = ""
                        article_fields["workerid"] = article_id
                        article_fields["title"] = article_title

                        article_fields["banner"] = 0
                        article_fields["specialtopic"] = 1
                        article_fields["topicid"] = topicid
                        article_fields["topicTitle"] = topictitle
                        #请求普通新闻详情

                        aurl = "https://app.shangshuitv.com//mag/info/v1/info/infoView?mag_hide_progress=1&themecolor=D00403&id="+str(article_id)
                        aheaders = {
                            "method": "GET",
                            "authority": "app.shangshuitv.com",
                            "scheme": "https",
                            "pragma": "no-cache",
                            "cache-control": "no-cache",
                            "upgrade-insecure-requests": "1",
                            "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 MAGAPPX|4.6.2-3.1.0-13|Android 6.0.1 Android MuMu|shangshuitv|X9IAiiXGUg4DAGSKJgN0nZPA|aa57db95f7dcaa53adbb476e07a1d1e2|8f4fd4cada121910a2b1d135ccaee772",
                            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                            "accept-encoding": "gzip, deflate",
                            "accept-language": "zh-CN,en-US;q=0.8",
                            "cookie": "PHPSESSID=ind2qggahnih4pb7uuabq90dv1",
                            "x-requested-with": "com.xinshangshui.app"
                        }
                        adata = {}
                        openurl = "https://app.shangshuitv.com//mag/info/v1/info/infoView?id=" + str(
                            article_id) + "&mag_hide_progress=1&themecolor=D00403"
                        article_fields["url"] = openurl

                        res = requests.get(aurl, headers=aheaders, data=adata)

                        try:
                            tree = html.fromstring(res.text)
                            name = tree.xpath('//div[@id="htmlData"]')
                            name1 = html.tostring(name[0])
                            content = HTMLParser().unescape(name1.decode())
                            article_fields["content"] = content
                            article_fields["appname"] = self.newsname

                            article_fields["videocover"] = []
                            article_fields["videos"] = []
                            article_fields["pubtime"] = 0
                            article_fields["createtime"] = 0
                            article_fields["updatetime"] = 0

                            try:
                                videos = InitClass().get_video(content)
                                article_fields["videos"] = videos
                            except Exception as e:
                                print("无视频 ")

                            try:
                                images = InitClass().get_images(content)
                                article_fields["images"] = images
                            except Exception as e:
                                print("无tupian")

                            print("专题文章==", json.dumps(article_fields, indent=4, ensure_ascii=False))
                        except Exception as e:
                            print("eee res==", res)

                    fields["articleIDs"] = articleids
                    fields["platformName"] = self.newsname
                    fields["platformID"] = ""

                    if topiclist:
                        firtstitem = topiclist[0]
                        newestarticleiD = firtstitem["id"]
                        fields["newestArticleID"] = newestarticleiD
                        fields["newestPubtime"] = 0
                    fields["pubTime"] = 0
                    fields["createTime"] = 0
                    fields["updateTime"] = 0

                    print("专题==", json.dumps(fields, indent=4, ensure_ascii=False))

                except Exception as e:
                    num += 1
                    logging.info(f"专题错误数量{num},{e}")
            else:
                try:

                    res = article.get("articleres")

                    try:
                        tree = html.fromstring(res)
                        name = tree.xpath('//div[@id="htmlData"]')
                        name1 = html.tostring(name[0])
                        content = HTMLParser().unescape(name1.decode())

                        fields["content"] = content
                        fields["appname"] = self.newsname
                        fields["channelType"] = ""

                        fields["videocover"] = []

                        fields["pubtime"] = 0
                        fields["createtime"] = 0
                        fields["updatetime"] = 0

                        fields["videos"] = []
                        try:
                            fields["content"] = content
                            videos = InitClass().get_video(content)
                            fields["videos"] = videos
                        except Exception as e:
                            print("无视频 ")

                        try:
                            images = InitClass().get_images(content)
                            fields["images"] = images
                        except Exception as e:
                            print("无tupian")

                        print("文章==", json.dumps(fields, indent=4, ensure_ascii=False))
                    except Exception as e:
                        print("eee res==",res)

                except Exception as e:
                    num += 1
                    logging.info(f"普通文章错误数量{num},{e}")

    def run(self):
        appparams = self.get_app_params()
        channelsres = self.getchannels(appparams.__next__())
        channelsparams = self.analyze_channel(channelsres.__next__())
        articlelistparames = self.getarticlelistparams(channelsparams.__next__())
        articleslistsres = self.getarticlelists(articlelistparames.__next__())
        articles = self.analyze_articlelists(articleslistsres.__next__())
        articleparams = self.getarticleparams(articles.__next__())
        articlesres = self.getarticlehtml(articleparams.__next__())
        self.analyzearticle(articlesres.__next__())


if __name__ == '__main__':
    appspider = XinHuNan("新商水")
    appspider.run()
