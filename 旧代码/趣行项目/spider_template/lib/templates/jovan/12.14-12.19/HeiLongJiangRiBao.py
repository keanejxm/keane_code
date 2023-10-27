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
#运行不通

def hasChannelInparam(channelparams, channelId, channelName):
    for channelParam in channelparams:
        if channelId == channelParam.get("channelid") and channelName == channelParam.get("channelname"):
            return True
    return False


def getChannelByRecursive(channelparams, channel):
    if "child" in channel and len(channel['child']):
        for channelChild in channel['child']:
            channelid = channelChild['id']
            channelname = channelChild['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)
            getChannelByRecursive(channelparams, channelChild)
    else:
        if hasChannelInparam(channelparams, channel['id'], channel['name']):
            pass
        else:
            channelid = channel['id']
            channelname = channel['name']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)


class HeiLongJiangRiBao(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://sjdb.hljnews.cn:8080/DBNewsAppService_v1.3.0/getListCategoryNew.do?flag=1"
        # 频道请求头
        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
            "Host": "sjdb.hljnews.cn:8080",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        # 频道数据体
        # data = {}
        # 如果携带的是json数据体,用appjson发送
        # app_json = {}
        # 频道请求方式
        method = "post"
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
        channelParamRecommd = InitClass().channel_fields(1, '推荐')
        channelparams.append(channelParamRecommd)
        for channel in channelslists['listCategory']:
            getChannelByRecursive(channelparams, channel)
        channelParamTopic = InitClass().channel_fields('qxdataTopic', '专题')
        channelparams.append(channelParamTopic)
        channelParamTopic = InitClass().channel_fields('98', '医事')
        channelparams.append(channelParamTopic)
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
            url = ''
            headers = {
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
                "Host": "sjdb.hljnews.cn:8080",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
            }
            # 频道数据体{"appid":"gxb","categoryId":"wz/dfdt/","lang":"cn","page":"1","pageSize":"10","plat":"a","version":"5.0"}
            data = {}
            # 如果携带的是json数据体,用appjson发送
            # channeljson = { }
            method = 'get'
            if 'qxdataTopic' == channelid:
                url = 'http://sjdb.hljnews.cn:8080/DBNewsAppService_v1.3.0/subjectList.do'
                data = {
                    # "cid": channelid,
                    "count": "10",
                    "startid": "-1",
                }
            else:
                url = 'http://sjdb.hljnews.cn:8080/DBNewsAppService_v1.3.0/getNewsList.do'
                data = {
                    "cid": channelid,
                    "count": "10",
                    "startid": "-1",
                }
            # 若数据体以json形式发送则以下面方式发送数据上面方式注释
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data)
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
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                # 可在下面打印处打断点，查看请求到的数据
                print(articlelist_json)
                # 若banner图在articlelist_json中则分来开取并给其复制banner = 1
                for item in articlelist_json['newslist']:
                    if 'listrunimage' in item and len(item['listrunimage']):
                        for article in item['listrunimage']:
                            articleparam = InitClass().article_list_fields()
                            articleparam["channelid"] = article['categoryid']
                            articleparam["channelname"] = channelname
                            articleparam["articleid"] = article['newsid']
                            articleparam["articletype"] = article['newsinfotype']
                            articleparam["articletitle"] = article['summary']
                            articleparam["banner"] = 1
                            articleparam["imageurl"] = article['imgpath']
                            articlesparams.append(articleparam)
                    else:
                        articleparam = InitClass().article_list_fields()
                        # articleparam["channelid"] = item['newsPubExt']['infotype']
                        articleparam["channelname"] = channelname
                        articleparam["articleid"] = item['newsPubExt']['newsid']
                        articleparam["articletype"] = item['newsPubExt']['infotype']
                        articleparam["articletitle"] = item['title']
                        articleparam["banner"] = 0
                        articleparam["imageurl"] = f"{article['imgpath']}/M_{article['imgname']}"
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
        url = ''
        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)",
            "Host": "sjdb.hljnews.cn:8080",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        # 频道数据体{"appid":"gxb","categoryId":"wz/dfdt/","lang":"cn","page":"1","pageSize":"10","plat":"a","version":"5.0"}
        data = {}
        method = 'get'
        for articleparam in articles:
            articletype = articleparam.get("articletype")
            if 2 == articletype:  # 专题
                print(articleparam)
                url = 'http://sjdb.hljnews.cn:8080/DBNewsAppService_v1.3.0/getNewsList.do'
                data = {
                    "sid": articleparam.get("articleid"),
                    "count": "10",
                    "startid": "-1",
                }
            else:
                print(articleparam)
                url = 'http://sjdb.hljnews.cn:8080/DBNewsAppService_v1.3.0/getNewsById.do'
                data = {
                    "newsid": articleparam.get("articleid"),
                    "memberid": "-1",
                    "device": "0000000059222d710337651200000000",
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
            articletitle = articleparam.get("articletitle")
            # 若APP有关于时间的反爬加sleeptime = 1，若发送为json数据体，则添加articlejson = articlejson
            article_show = InitClass().article_params_fields(url, headers, method, channelname, imgurl,
                                                             data=data,
                                                             videourl=videos, videocover=videocover, pubtime=pubtime,
                                                             createtime=createtime, updatetime=updatetime,
                                                             source=source, author=author, likenum=likenum,
                                                             commentnum=commentnum, sharenum=articletitle,
                                                             readnum=articletype,
                                                             articleid=articleid, articleurl=articleurl, banners=banner)
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
            articletype = articleResponse.get("readnum")  # 没有articletype属性，使用readnum属性代替。
            articletitle = articleResponse.get("sharenum")  # articletitle，使用sharenum属性代替。
            commentnum = articleResponse.get("commentnum")
            banner = articleResponse.get("banner")
            articleres = articleResponse.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            # fields["imageurl"] = imageurl
            fields["banner"] = banner
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                print(articlejson)

                fields["appname"] = appname
                if 2 == articletype:
                    print(articlejson)
                    # fields["url"] = articlejson['data']['pageUrl']  # 文章的html网址，提取shareurl
                    fields["workerid"] = articleid  # 文章的id
                    fields["title"] = articletitle  # 文章的标题
                    fields["content"] = articlejson['newslist']  # 文章的内容详情

                    fields["articlecovers"] = imageurl  # 文章的封面，一般为上面get到的字段
                    # fields["images"] = imageurl  # 文章详情内的图片url，一般为列表需遍历获取
                    # fields["videos"] = articlejson['data']['videoUrl']  # 文章的视频链接地址
                    # fields["videocover"] = articlejson['data']['link']  # 文章的视频封面地址
                    # fields["width"] = articlejson['data']['link']  # 文章的视频宽
                    # fields["height"] = articlejson['data']['link']  # 文章的视频高
                    fields["source"] = source  # 文章的来源
                    fields["pubtime"] = pubtime  # 文章的发布时间
                    # fields["createtime"] = articlejson['data']['createDate']  # 文章的发布时间
                    # fields["updatetime"] = articlejson['data']['pubDate']  # 文章的更新时间
                    # fields["likenum"] = articlejson['data']['newsPubExt']['supportcount']  # 文章的点赞数
                    # fields["playnum"] = articlejson['data']['link']  # 视频的播放数
                    # fields["commentnum"] = len(articlejson['data']['comments'])  # 文章评论数
                    # fields["readnum"] = articlejson['data']['newsPubExt']['clickcount']  # 文章的阅读数
                    # fields["trannum"] = articlejson['data']['newsPubExt']['reviewcount']  # 文章的转发数
                    # fields["sharenum"] = articlejson['data']['link']  # 文章分享数
                    # fields["author"] = articlejson['data']['author']  # 文章作者
                else:
                    # fields["url"] = articlejson['data']['pageUrl']  # 文章的html网址，提取shareurl
                    fields["workerid"] = articlejson['data']['newsPubExt']['newsid']  # 文章的id
                    fields["title"] = articlejson['data']['title']  # 文章的标题
                    fields["content"] = articlejson['data']['htmlbody']  # 文章的内容详情

                    # fields["articlecovers"] = articlejson['data']['img']  # 文章的封面，一般为上面get到的字段
                    fields["images"] = InitClass().get_images(fields["content"])   # 文章详情内的图片url，一般为列表需遍历获取
                    # fields["videos"] = articlejson['data']['videoUrl']  # 文章的视频链接地址
                    # fields["videocover"] = articlejson['data']['link']  # 文章的视频封面地址
                    # fields["width"] = articlejson['data']['link']  # 文章的视频宽
                    # fields["height"] = articlejson['data']['link']  # 文章的视频高
                    fields["source"] = articlejson['data']['source']  # 文章的来源
                    fields["pubtime"] = articlejson['data']['publishtime']  # 文章的发布时间
                    # fields["createtime"] = articlejson['data']['createDate']  # 文章的发布时间
                    # fields["updatetime"] = articlejson['data']['pubDate']  # 文章的更新时间
                    fields["likenum"] = articlejson['data']['newsPubExt']['supportcount']  # 文章的点赞数
                    # fields["playnum"] = articlejson['data']['link']  # 视频的播放数
                    # fields["commentnum"] = len(articlejson['data']['comments'])  # 文章评论数
                    fields["readnum"] = articlejson['data']['newsPubExt']['clickcount']  # 文章的阅读数
                    fields["trannum"] = articlejson['data']['newsPubExt']['reviewcount']  # 文章的转发数
                    # fields["sharenum"] = articlejson['data']['link']  # 文章分享数
                    fields["author"] = articlejson['data']['author']  # 文章作者
                    if len(articlejson['data']['listaudio']):
                        print(articlejson)
                        fields[
                            "videos"] = f"{articlejson['data']['listaudio'][0]['filePath']}/{articlejson['data']['listaudio'][0]['fileName']}"  # 文章的视频链接地址
                        fields[
                            "videocover"] = f"{articlejson['data']['listaudio'][0]['filePath']}/{articlejson['data']['listaudio'][0]['fileName']}.jpg"  # 文章的视频封面地址

                    if len(articlejson['data']['listpic']):
                        print(articlejson)
                        imgs = list()
                        for temp in articlejson['data']['listpic']:
                            imgs.append(f"{temp['filePath']}/M_{temp['fileName']}")
                        fields["images"] = imgs  # 文章详情内的图片url，一般为列表需遍历获取
                    if len(articlejson['data']['listreview']):
                        print(articlejson)
                    if len(articlejson['data']['listrunimage']):
                        print(articlejson)
                    if len(articlejson['data']['listvedio']):
                        print(articlejson)
                        fields[
                            "videos"] = f"{articlejson['data']['listvedio'][0]['filePath']}/{articlejson['data']['listvedio'][0]['fileName']}"  # 文章的视频链接地址
                        fields[
                            "videocover"] = f"{articlejson['data']['listvedio'][0]['filePath']}/{articlejson['data']['listvedio'][0]['fileName']}.jpg"  # 文章的视频封面地址

                    if len(articlejson['data']['listvote']):
                        print(articlejson)

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
    spider = HeiLongJiangRiBao('黑龙江日报')
    spider.run()
