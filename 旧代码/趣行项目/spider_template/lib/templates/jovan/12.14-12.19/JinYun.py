# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging

import requests

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


def setArticleListParam(channelname, channelid, banner, articleparam, article):
    articleparam["channelname"] = channelname
    articleparam["channelid"] = channelid
    articleparam["articleid"] = article['jsonUrl']
    articleparam["articletype"] = article['newsType']
    articleparam["articletitle"] = article['title']
    # articleparam["channelname"] = article['title']
    articleparam["banner"] = banner
    articleparam["imageurl"] = article['guideImage2']
    # articleparam["articleurl"] = article['title']
    if 'videos' in article.keys() and len(article['videos']):
        articleparam["videos"] = article['videos'][0]['url']
    # articleparam["videos"] = article['title']
    # articleparam["videocover"] = article['title']
    articleparam["pubtime"] = article['pubDate']
    # articleparam["createtime"] = article['createDate']
    # articleparam["updatetime"] = article['title']
    articleparam["source"] = article['sourceName']
    # articleparam["author"] = article['author']
    # articleparam["likenum"] = article['digg']
    # articleparam["commentnum"] = article['pl']
    # articleparam["readnum"] = article['title']
    # articleparam["sharenum"] = article['title']
    return articleparam


class JinYun(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        GET https://static20.app.tjyun.com/cms_cate/top_all_ctg.json HTTP/1.1
        User-Agent: JinYunApp/2.8.14/Android 6.0.1/Netease/MuMu
        Host: static20.app.tjyun.com
        Connection: Keep-Alive
        Accept-Encoding: gzip
        """
        # 频道url
        url = "https://static20.app.tjyun.com/cms_cate/top_all_ctg.json"
        # 频道请求头
        headers = {
            "User-Agent": "JinYunApp/2.8.14/Android 6.0.1/Netease/MuMu",
            "Host": "static20.app.tjyun.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        # 频道数据体
        # data = {}
        # 如果携带的是json数据体,用appjson发送
        # app_json = {}
        # 频道请求方式
        method = "get"
        app_params = InitClass().app_params(url, headers, method)
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
        for channel in channelslists['result']['data']:
            channelparam = InitClass().channel_fields(channel['guideListUrl'], channel['categoryName'])
            channelparams.append(channelparam)
            if 'children' in channel and len(channel['children']):
                for channelChild in channel['children']:
                    channelparam = InitClass().channel_fields(channelChild['guideListUrl'],
                                                              channel['categoryName'] + "-" + channelChild[
                                                                  'categoryName'])
                    channelparams.append(channelparam)

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
            # 频道请求头
            headers = {
                "User-Agent": "JinYunApp/2.8.14/Android 6.0.1/Netease/MuMu",
                "Host": "static20.app.tjyun.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
            }
            # 频道数据体
            # data = {}
            # 如果携带的是json数据体,用appjson发送
            # app_json = {}
            # 频道请求方式
            method = "get"
            # 若数据体以json形式发送则以下面方式发送数据上面方式注释
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channelid=channelid)
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
            channelname = articleslist_res.get("channelname")
            channelid = articleslist_res.get("channelid")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                # 可在下面打印处打断点，查看请求到的数据
                print(articlelist_json)
                for articlelist in articlelist_json['result']['data']:
                    if articlelist['cardStyleId'] == '480':
                        for newsItem in articlelist['newsList']:
                            articleparam = InitClass().article_list_fields()
                            articleparam = setArticleListParam(channelname, channelid, 1, articleparam, newsItem);
                            articlesparams.append(articleparam)
                    else:
                        for newsItem in articlelist['newsList']:
                            articleparam = InitClass().article_list_fields()
                            articleparam = setArticleListParam(channelname, channelid, 0, articleparam, newsItem);
                            articlesparams.append(articleparam)
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
        url = ""
        # 频道请求头
        headers = {
            "User-Agent": "JinYunApp/2.8.14/Android 6.0.1/Netease/MuMu",
            "Host": "static20.app.tjyun.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        # 频道数据体
        # data = {}
        # 如果携带的是json数据体,用appjson发送
        # app_json = {}
        # 频道请求方式
        method = "get"
        for articleparam in articles:
            url = articleparam.get("articleid")

            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            channelid = articleparam.get("channelid")
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
            article_show = InitClass().article_params_fields(url, headers, method, channelname, imgurl, videourl=videos,
                                                             videocover=videocover, pubtime=pubtime,
                                                             createtime=createtime, updatetime=updatetime,
                                                             source=source, author=author, likenum=likenum,
                                                             commentnum=channelid, sharenum=sharenum,
                                                             readnum=readnum,
                                                             articleid=articleid, articleurl=articleurl, banners=banner)
            articlesparam.append(article_show)
        yield articlesparam

    @staticmethod
    def analyzearticles(articles_res):
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            articleid = articleres.get("articleid")
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            articletype = articleres.get("readnum")  # 没有articletype属性，使用readnum属性代替。
            channelid = articleres.get("commentnum")  # 没有articletype属性，使用readnum属性代替。
            # 若上面存储了此字段需用下列方式获取
            # videos = articleres.get("videos")
            # videocover = articleres.get("videocover")
            # pubtime = articleres.get("pubtime")
            # createtime = articleres.get("createtime")
            # updatetime = articleres.get("updatetime")
            # source = articleres.get("source")
            # likenum = articleres.get("author")
            # commentnum = articleres.get("author")
            # sharenum = articleres.get("sharenum")
            # readnum = articleres.get("readnum")
            # author = articleres.get("author")
            # articleurl = articleres.get("articleurl")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelID"] = channelid
            # fields["imageurl"] = imgurl
            fields["banner"] = banners
            # 如果有下列字段需添加
            # fields["url"] = articleurl #文章的html网址，提取shareurl
            # fields["workerid"] = workerid #文章的id
            # fields["title"] = title #文章的标题
            # fields["content"] = content #文章的内容详情
            # fields["articlecovers"] = imgurl #文章的封面，一般为上面get到的字段
            # fields["images"] = iamges #文章详情内的图片url，一般为列表需遍历获取
            # fields["videos"] = videos #文章的视频链接地址
            # fields["videocover"] = videocover #文章的视频封面地址
            # fields["width"] = width #文章的视频宽
            # fields["height"] = height #文章的视频高
            # fields["source"] = source #文章的来源
            # fields["pubtime"] = pubtime #文章的发布时间
            # fields["createtime"] = createtime #文章的发布时间
            # fields["updatetime"] = updatetime #文章的更新时间
            # fields["likenum"] = likenum #文章的点赞数
            # fields["playnum"] = playnum #视频的播放数
            # fields["commentnum"] = commentnum #文章评论数
            # fields["readnum"] = readnum #文章的阅读数
            # fields["trannum"] = trannum #文章的转发数
            # fields["sharenum"] = sharenum #文章分享数
            # fields["author"] = author #文章作者
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                print(articlejson)

                fields["appname"] = appname

                fields["channelID"] = articlejson['result']['data']['categoryId']  # 文章的html网址，提取shareurl
                fields["url"] = articlejson['result']['data']['detailUrl']  # 文章的html网址，提取shareurl
                fields["workerid"] = articlejson['result']['data']['newsId']  # 文章的id
                fields["title"] = articlejson['result']['data']['title']  # 文章的标题
                if '20000' == articlejson['result']['data']['newsType']:  # 专题
                    fields["content"] = json.dumps(articlejson['result']['data']['guideInfo'])  # 文章的内容详情
                else:
                    fields["content"] = articlejson['result']['data']['content']  # 文章的内容详情

                fields["articlecovers"] = [articlejson['result']['data']['guideImage2']]  # 文章的封面，一般为上面get到的字段
                fields["images"] = InitClass().get_images(fields["content"])  # 文章详情内的图片url，一般为列表需遍历获取

                if 'videos' in articlejson['result']['data'].keys() and len(articlejson['result']['data']['videos']):
                    fields["videos"] = [articlejson['result']['data']['videos'][0]['url']]
                # fields["videos"] = articlejson['result']['data']  # 文章的视频链接地址
                # fields["videocover"] = articlejson['result']['data']  # 文章的视频封面地址
                # fields["width"] = articlejson['result']['data']  # 文章的视频宽
                # fields["height"] = articlejson['result']['data']  # 文章的视频高
                fields["source"] = articlejson['result']['data']['sourceName']  # 文章的来源
                fields["pubtime"] = articlejson['result']['data']['pubDate']  # 文章的发布时间
                # fields["createtime"] = articlejson['result']['data']  # 文章的发布时间
                # fields["updatetime"] = articlejson['result']['data'] # 文章的更新时间
                fields["likenum"] = articlejson['result']['data']['praiseCount']  # 文章的点赞数
                # fields["playnum"] = articlejson['result']['data']  # 视频的播放数
                # fields["commentnum"] = articlejson['result']['data']  # 文章评论数
                # fields["readnum"] = articlejson['result']['data']  # 文章的阅读数
                # fields["trannum"] = articlejson['result']['data']  # 文章的转发数
                # fields["sharenum"] = articlejson['result']['data']  # 文章分享数
                # fields["author"] = articlejson['result']['data']  # 文章作者

                print(json.dumps(fields, indent=4, ensure_ascii=False))
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
    spider = JinYun('津云')
    spider.run()
