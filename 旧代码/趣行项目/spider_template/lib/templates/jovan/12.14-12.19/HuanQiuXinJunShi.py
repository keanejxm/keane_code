# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging

import bs4

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass
#视频没有内容

def setArticleListParam(channelname, articleparam, article):
    articletitle = article['title']
    articleid = article['aid']
    articleparam["channelid"] = article['channel']
    articleparam["channelname"] = channelname
    articleparam["articleid"] = article['aid']
    articleparam["articletype"] = article['news_show_type']
    articleparam["articletitle"] = article['title']
    # articleparam["channelname"] = article['title']
    # articleparam["banner"] = article['title']
    articleparam["imageurl"] = article['image']
    # articleparam["articleurl"] = article['title']
    # articleparam["videos"] = article['title']
    # articleparam["videocover"] = article['title']
    articleparam["pubtime"] = article['pubDate']
    # articleparam["createtime"] = article['title']
    # articleparam["updatetime"] = article['title']
    # articleparam["source"] = article['title']
    articleparam["author"] = article['author']
    articleparam["likenum"] = article['digg']
    articleparam["commentnum"] = article['pl']
    # articleparam["readnum"] = article['title']
    # articleparam["sharenum"] = article['title']
    return articleparam


class HuanQiuXinJunShi(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://if02.hangkong.com/api2.5/app.php?"
        # 频道请求头
        headers = {
            "Content-Length": "44",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "if02.hangkong.com",
            "Connection": "Keep-Alive",
            "Cookie": "ad_small_num=3; channel=xiaomi",
            "Cookie2": "$Version=1",
            "Accept-Encoding": "gzip",
            "User-Agent": "xinjunshi/2.5.2(android)",
        }
        # 频道数据体
        data = {
            "mod": "newslist",
            "act": "index",
            "page": "1",
            "newid": "621883",
        }
        # 如果携带的是json数据体,用appjson发送
        app_json = {'devicetoken=805e3735c9c1b06b626d18476efaf693'}
        # 频道请求方式
        method = "post"
        app_params = InitClass().app_params(url, headers, method, data = data, appjson = app_json)
        # 如果携带json数据，用下列方式存储发送数据
        # app_params = InitClass().app_params(url, headers, method, data = data ,appjson=app_json)
        yield app_params

    @staticmethod
    def analyzechannels(channelsres):
        """
        此方法主要获取channelid,channelname即可
        若请求文章列表页需要channeltype，categoryname，categoryid,则以categoryname= categoryname形式传递参数
        :param channelsres:
        :return:
        """
        # 将返回的数据转为json数据
        channelslists = json.loads(channelsres)
        # 返回的数据是编码错误，则用下面代码解析数据
        # channelslists = json.loads(json.dumps(channelsres,indent=4,ensure_ascii=False))
        print(channelslists)
        channelparams = []
        for channel in channelslists['data']['nav']:
            channelid = 'http://if02.hangkong.com/api2.5/' + channel['url']
            channelname = channel['name']
            if 'showtype' in channel.keys() and channel['showtype'] == 3:  # 这个是外来数据，直接调用的百度的url，采不到列表，直接略过
                print('外来列表：', channel)
                continue
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)
        bottomVideoParam = InitClass().channel_fields(
            'http://if02.hangkong.com/api2.5/app.php?mod=exclusivelist&act=index&page=1&newid=608619 ', '底部视频')
        channelparams.append(bottomVideoParam)
        yield channelparams

    @staticmethod
    def getarticlelistsparams(channelsparams):
        """
        此方法目的是组建请求文章列页面数据参数，url，headers，data，若以json形式发送数据，则channeljson = channeljson
        :param channelsparams:
        :return:
        """
        articleparams = []
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            url = channelid
            headers = {
                "Content-Length": "44",
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "if02.hangkong.com",
                "Connection": "Keep-Alive",
                "Cookie": "ad_small_num=6; channel=xiaomi",
                "Cookie2": "$Version=1",
                "Accept-Encoding": "gzip",
                "User-Agent": "xinjunshi/2.5.2(android)",
            }
            data = {
                "page": "1",
                # "newid": "621414",
            }
            # 如果携带的是json数据体,用appjson发送
            channeljson = {'devicetoken=805e3735c9c1b06b626d18476efaf693'}
            method = 'post'
            # 若数据体以json形式发送则以下面方式发送数据上面方式注释
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,
                                                                       channeljson = channeljson)
            articleparams.append(articlelist_param)
        yield articleparams

    @staticmethod
    def analyze_articlelists(articleslist_ress):
        """
        解析文章列表页，目的是为了获取文章具体信息，组建请求文章详情数据体
        :param articleslist_ress:
        :return:
        """
        articlesparams = []
        for articleslist_res in articleslist_ress:
            banners = articleslist_res.get("banner")
            channelname = articleslist_res.get("channelname")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                # 可在下面打印处打断点，查看请求到的数据
                print(articlelist_json)
                # 若banner图在articlelist_json中则分来开取并给其复制banner = 1
                try:
                    articlelists = articlelist_json['data']['item']
                    for article in articlelists:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        print(article)
                        if 'ad_type' in article.keys():
                            # print('列表过滤广告：', article)
                            continue
                        else:
                            articleparam = InitClass().article_list_fields()
                            articleparam = setArticleListParam(channelname, articleparam, article);
                            articlesparams.append(articleparam)
                    slidelists = articlelist_json['data']['slide']
                    for article in slidelists:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        print(article)
                        if 'ad_type' in article.keys():
                            # print('列表过滤广告：', article)
                            continue
                        else:
                            articleparam = InitClass().article_list_fields()
                            articleparam = setArticleListParam(channelname, articleparam, article);
                            articleparam["banner"] = 1
                            articlesparams.append(articleparam)
                    toplists = articlelist_json['data']['top']
                    for article in toplists:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        print(article)
                        if 'ad_type' in article.keys():
                            # print('列表过滤广告：', article)
                            continue
                        else:
                            articleparam = InitClass().article_list_fields()
                            articleparam = setArticleListParam(channelname, articleparam, article);
                            articlesparams.append(articleparam)
                except Exception as e:
                    print(e, articlelist_json)
            except Exception as e:
                print(e, articlelist_json)
        yield articlesparams

    @staticmethod
    def getarticleparams(articles):
        """
        组建请求文章详情所需要的数据体
        :param articles:
        :return:
        """
        articlesparam = []
        url_show = 'http://if02.hangkong.com/api2.5/app.php?'
        headers = {
            "Accept ": "*/* ",
            "Accept-Encoding ": "gzip, deflate ",
            "Accept-Language ": "zh-cn ",
            "Content-Length ": "44 ",
            "Content-Type ": "application/x-www-form-urlencoded ",
            "Host ": "if02.hangkong.com ",
            "Connection ": "Keep-Alive ",
            "Cookie ": "ad_small_num=3; channel=xiaomi ",
            "Cookie2 ": "$Version=1 ",
            "User-Agent ": "xinjunshi/2.5.2(android) ",
        }

        # 如果携带的是json数据体,用appjson发送
        article_json = {'devicetoken=805e3735c9c1b06b626d18476efaf693'}
        method = 'get'
        for articleparam in articles:
            data_show = {
                "mod": "show",
                "aid": articleparam.get('articleid'),
                "type": articleparam.get('channelid'),
                # "newid": "621414",
            }
            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            articleid = articleparam.get("articleid")
            banner = articleparam.get("banner")
            imgurl = articleparam.get("imageurl")
            videos = articleparam.get("videos")
            videocover = articleparam.get("videocover")
            pubtime = articleparam.get("pubtime")
            createtime = articleparam.get("createtime")
            updatetime = articleparam.get("updatetime")
            source = articleparam.get("source")
            author = articleparam.get("author")
            likenum = articleparam.get("likenum")
            commentnum = articleparam.get("commentnum")
            sharenum = articleparam.get("sharenum")
            readnum = articleparam.get("readnum")
            articleurl = articleparam.get("articleurl")
            # 若APP有关于时间的反爬加sleeptime = 1，若发送为json数据体，则添加articlejson = articlejson
            article_show = InitClass().article_params_fields(url_show, headers, method, channelname, imgurl,
                                                             data = data_show,
                                                             videourl = videos, videocover = videocover,
                                                             pubtime = pubtime,
                                                             createtime = createtime, updatetime = updatetime,
                                                             source = source, author = author, likenum = likenum,
                                                             commentnum = commentnum, sharenum = sharenum,
                                                             readnum = readnum,
                                                             articleid = articleid, articleurl = articleurl,
                                                             banners = banner,
                                                             articlejson = article_json)
            articlesparam.append(article_show)
        yield articlesparam

    @staticmethod
    def analyzearticles(articleResponseData):
        for articleResponse in articleResponseData:
            appname = articleResponse.get("appname")
            channelname = articleResponse.get("channelname")
            imageurl = articleResponse.get("imageurl")
            videourl = articleResponse.get("videourl")
            videocover = articleResponse.get("videocover")
            articleurl = articleResponse.get("articleurl")
            articleid = articleResponse.get("articleid")
            pubtime = articleResponse.get("pubtime")
            createtime = articleResponse.get("createtime")
            updatetime = articleResponse.get("updatetime")
            source = articleResponse.get("source")
            author = articleResponse.get("author")
            likenum = articleResponse.get("likenum")
            readnum = articleResponse.get("readnum")
            sharenum = articleResponse.get("sharenum")
            commentnum = articleResponse.get("commentnum")
            banner = articleResponse.get("banner")
            articleres = articleResponse.get("articleres")
            # fields = InitClass().article_fields()
            # fields["channelname"] = channelname
            # fields["imageurl"] = imageurl
            # fields["banner"] = banner
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent = 4, ensure_ascii = False))
                print(articlejson)
                content = ""
                if 'content' in articlejson['data'].keys():
                    content = ''.join(articlejson['data']['content'])

                videoUrl = ""
                if 'video_html' in articlejson['data'].keys():
                    video_html = articlejson['data']['video_html']
                    bf = bs4.BeautifulSoup(video_html, 'html.parser')
                    videoUrl = bf.find('iframe')['src']

                fields = InitClass().article_fields()
                fields["appname"] = appname  # 应用名称，字符串
                fields["channelname"] = channelname  # 频道名称，字符串
                fields["channelID"] = articlejson['data']['channel']  # 频道id，字符串
                fields["channelType"] = ""  # 频道type，字符串
                fields["url"] = articlejson['data']['link']  # 分享的网址，字符串
                fields["workerid"] = articleid  # 文章id，字符串
                fields["title"] = articlejson['data']['title']  # 文章标题，字符串
                fields["content"] = content  # 文章内容，字符串
                fields["articlecovers"] = [] if not articlejson['data']['image'] else [
                    articlejson['data']['image']]  # 列表封面，数组
                fields["images"] = articlejson['data']['pics']  # 正文图片，数组
                fields["videos"] = [] if not videoUrl else [videoUrl]  # 视频地址，数组
                fields["videocover"] = []  # 视频封面，数组
                fields["width"] = ""  # 视频宽，字符串
                fields["height"] = ""  # 视频高，字符串
                fields["source"] = articlejson['data']['category']  # 文章来源，字符串
                fields["pubtime"] = InitClass().date_time_stamp(articlejson['data']['pubDate'])  # 发布时间，时间戳（毫秒级，13位）
                fields["createtime"] = 0  # 创建时间，时间戳（毫秒级，13位）
                fields["updatetime"] = 0  # 更新时间，时间戳（毫秒级，13位）
                fields["likenum"] = int(articlejson['data']['goodpost'])  # 点赞数（喜欢数），数值
                fields["playnum"] = 0  # 播放数，数值
                fields["commentnum"] = len(articlejson['data']['comments'])  # 评论数，数值
                fields["readnum"] = int(articlejson['data']['click'])  # 阅读数，数值
                fields["trannum"] = 0  # 转发数，数值
                fields["sharenum"] = 0  # 分享数，数值
                fields["author"] = articlejson['data']['author']  # 作者，字符串
                fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                fields["specialtopic"] = 0  # 是否是专题，数值（0标识不是，1标识是）
                fields["topicid"] = ""  # 专题id，字符串

                print(json.dumps(fields, indent = 4, ensure_ascii = False))
            except Exception as e:
                print(e)

    def run(self):
        appparams = self.get_app_params()
        channelsres = self.getchannels(appparams.__next__())
        channelsparams = self.analyzechannels(channelsres.__next__())
        articleparams = self.getarticlelistsparams(channelsparams.__next__())
        articles_ress = self.getarticlelists(articleparams.__next__())
        articles = self.analyze_articlelists(articles_ress.__next__())
        articlesparam = self.getarticleparams(articles.__next__())
        articles_html = self.getarticlehtml(articlesparam.__next__())
        self.analyzearticles(articles_html.__next__())


if __name__ == '__main__':
    spider = HuanQiuXinJunShi('环球新军事')
    spider.run()
