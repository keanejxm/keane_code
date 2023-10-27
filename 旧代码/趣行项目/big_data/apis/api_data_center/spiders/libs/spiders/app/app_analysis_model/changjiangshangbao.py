# -*- encoding:utf-8 -*-
"""
@功能:新湖南解析模板
@AUTHOR：fred
@文件名：xinhunan.py
@时间：2020/12/17  17:33
"""

import json
import logging
from lxml import etree

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class Changjiangshangbao(Appspider):

    @staticmethod
    def get_app_params():
        url = "http://cjsb.chenjian1982.cn/appdata/index.php?type=getsort&token=Z4CsopwWqAdx0857F6"
        headers = {
            "Charset": "UTF-8",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 CJSBAPP",
            "Accept-Encoding": "gzip",
            "Cookie": "USR=9urtbx5n%090%091610244449%09http%3A%2F%2Fcjsb.chenjian1982.cn%2Fappdata%2Findex.php%3Ftype%3Dsortupdate%26token%3DZ4CsopwWqAdx0857F6",
            "Host": "cjsb.chenjian1982.cn",
            "Connection": "keep-alive",
        }
        data = {}
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data=data)
        yield app_params

    @staticmethod
    def analyze_channel(channelsres):
        channelslists = json.loads(json.dumps(json.loads(channelsres), indent=4, ensure_ascii=False))
        index = 0
        for channel in channelslists:
            channelname = channel["name"]
            channelid = str(index)
            index += 1
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam
        channelname = "视频"
        channelid = "9"
        channelparam = InitClass().channel_fields(channelid, channelname)
        yield channelparam

    def getarticlelistparams(self, channelsres):
        channel_num = 0
        for channel in self.analyze_channel(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            channeltype = channel.get("channeltype")  # 此处没有若有可加上，其他一样
            url = "http://cjsb.chenjian1982.cn/appdata/index.php?type=list&token=Z4CsopwWqAdx0857F6&fid=" + channelid
            headers = {
                "Charset": "UTF-8",
                "Accept": "*/*",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 CJSBAPP",
                "Accept-Encoding": "gzip",
                "Cookie": "USR=9urtbx5n%090%091610245120%09http%3A%2F%2Fcjsb.chenjian1982.cn%2Fappdata%2Findex.php%3Ftype%3Dcontent%26token%3DZ4CsopwWqAdx0857F6%26aid%3D612249",
                "Host": "cjsb.chenjian1982.cn",
                "Connection": "keep-alive"
            }
            data = {}
            method = "get"
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            if channelname == "视频":
                url = "http://cjsb.chenjian1982.cn/appdata/index.php?type=list&mid=106&token=Z4CsopwWqAdx0857F6&fid=" + channelid

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid, data=data,
                                                                       channeltype=channeltype,
                                                                       channel_index_id=channel_index_id)
            if channelname == '头条':
                bannerurl = "http://cjsb.chenjian1982.cn/appdata/index.php?type=toutiao&token=Z4CsopwWqAdx0857F6&fid=undefined"
                banner_param = InitClass().articlelists_params_fields(bannerurl, headers, method, channelname,
                                                                      channelid=channelid, data=data,
                                                                      channeltype=channeltype, banners=1)
                yield channel_field, [articlelist_param, banner_param]
            else:
                yield channel_field, [articlelist_param]

    @staticmethod
    def analyze_articlelists(articleslistsres):
        for articleslistres in articleslistsres:
            channelname = articleslistres.get("channelname")
            channel_index_id = articleslistres.get("channelindexid")
            channelid = articleslistres.get("channelid")
            articleslists = articleslistres.get("channelres")
            banner = articleslistres.get("banner")
            try:
                articleslists = json.loads(json.dumps(json.loads(articleslists), indent=4, ensure_ascii=False))
                try:
                    contentlist = articleslists
                    for article in contentlist:
                        articleid = article["aid"]
                        article_fields = InitClass().article_fields()
                        article_fields["channelID"] = channelid
                        article_fields["channelname"] = channelname
                        article_fields["channelindexid"] = channel_index_id
                        article_fields["workerid"] = articleid
                        article_fields["banner"] = banner
                        article_fields["url"] = "http://m.changjiangtimes.com/?aid=" + str(articleid)
                        yield article_fields
                except Exception as e:
                    logging.info(f"提取文章列表信息失败{e, channelname}")
            except Exception as e:
                logging.info(f"解析文章列表{e}")

    def getarticleparams(self, articleslistsres):
        for article in self.analyze_articlelists(articleslistsres):
            articleid = article.get("workerid")
            channelname = article.get("channelname")
            url = "http://cjsb.chenjian1982.cn/appdata/index.php?type=content&token=Z4CsopwWqAdx0857F6&aid=" + articleid
            headers = {
                "Charset": "UTF-8",
                "Accept": "*/*",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 CJSBAPP",
                "Accept-Encoding": "gzip",
                "Cookie": "USR=9urtbx5n%090%091610245187%09http%3A%2F%2Fcjsb.chenjian1982.cn%2Fappdata%2Findex.php%3Ftype%3Dlist%26token%3DZ4CsopwWqAdx0857F6%26fid%3D2",
                "Host": "cjsb.chenjian1982.cn",
                "Connection": "keep-alive"
            }
            data = {}
            method = 'get'

            if channelname == '视频':
                url = "http://cjsb.chenjian1982.cn/appdata/index.php?type=getvideo&token=Z4CsopwWqAdx0857F6&aid=" + articleid
            articleparam = InitClass().article_params_fields(url, headers, method, data=data,
                                                             article_field=article)
            yield [articleparam]

    def analyzearticle(self, articleres):
        num = 0
        for article in articleres:
            fields = article.get("articleField")
            # topic = fields.get("topic")
            try:
                content_s = json.loads(
                    json.dumps(json.loads(article.get("articleres"), strict=False), indent=4, ensure_ascii=False))
                # print("content_s==",content_s)
                source = content_s["copyfrom"]
                content = content_s["content"]
                title = content_s["title"]
                pubtime = content_s["posttime"]
                pubtime = int(pubtime) * 1000

                try:
                    commentsnum = content_s["comments"]
                    fields["commentnum"] = commentsnum
                except Exception as e:
                    print("无评论")
                cover = content_s["picurl"]
                covers = list()
                if cover:
                    covers.append(cover)
                readnum = content_s["hits"]
                fields["title"] = title
                fields["articlecovers"] = covers
                fields["pubtime"] = pubtime
                fields["source"] = source
                fields["author"] = ""
                content = InitClass().wash_tag(content)
                fields["content"] = content
                fields["createtime"] = 0
                fields["updatetime"] = 0
                try:
                    videos = InitClass().get_video(content)
                    fields["videos"] = videos
                except Exception as e:
                    print("无视频")
                try:
                    images = list()
                    if "<img" in content:
                        content_tree = etree.HTML(content)
                        img_list = content_tree.xpath(".//img/@data-echo")
                        for img in img_list:
                            if img:
                                images.append(img)
                    fields["images"] = images
                except Exception as e:
                    print("无图片")
                fields["appname"] = self.newsname
                fields["platformID"] = self.platform_id
                fields["likenum"] = 0
                fields["readnum"] = readnum
                fields["sharenum"] = 0
                channelname = fields["channelname"]
                if channelname == "视频":
                    videourl = content_s["videourl"]
                    prevideolist = fields["videos"]
                    prevideolist.append(videourl)
                    fields["videos"] = prevideolist
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                num += 1
                logging.info(f"错误数量{num},{e}")

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = Changjiangshangbao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
