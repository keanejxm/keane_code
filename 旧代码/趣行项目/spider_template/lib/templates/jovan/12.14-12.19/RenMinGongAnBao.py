# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import logging
from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


def setArticleListParam(channelname, banner, articleparam, article):
    articleparam["channelid"] = article['url']
    articleparam["channelname"] = channelname
    articleparam["articleid"] = article['docid']
    # articleparam["articletype"] = article['news_show_type']
    articleparam["articletitle"] = article['title']
    articleparam["banner"] = banner
    if len(article['cimgs']) > 0:
        articleparam["imageurl"] = article['cimgs'][0]
    articleparam["articleurl"] = article['sharelink']
    articleparam["videos"] = article['videourl']
    # articleparam["videocover"] = article['title']
    articleparam["pubtime"] = article['updatedate']
    # articleparam["createtime"] = article['title']
    # articleparam["updatetime"] = article['title']
    if 'source' in article.keys():
        articleparam["source"] = article['source']
    # articleparam["author"] = article['author']
    # articleparam["likenum"] = article['digg']
    # articleparam["commentnum"] = article['pl']
    # articleparam["readnum"] = article['title']
    # articleparam["sharenum"] = article['title']
    return articleparam


class RenMinGongAnBao(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道请求头
        headers = {
            "Host": "www.cpd.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.0",
        }
        # 频道数据体
        # data = {}
        # 如果携带的是json数据体,用appjson发送
        # app_json = {}
        # 频道请求方式
        method = "get"
        # 频道url
        url1 = "http://www.cpd.com.cn/app/xw/channels.json"
        url2 = "http://www.cpd.com.cn/app/hd/channels.json"

        app_params1 = InitClass().app_params(url1, headers, method)
        app_params2 = InitClass().app_params(url2, headers, method)
        # 如果携带json数据，用下列方式存储发送数据
        # app_params = InitClass().app_params(url, headers, method, data = data ,appjson=app_json)
        yield [app_params1, app_params2]

    @staticmethod
    def analyzechannels(channelsres):
        """
        此方法主要获取channelid,channelname即可
        若请求文章列表页需要channeltype，categoryname，categoryid,则以categoryname= categoryname形式传递参数
        :param channelsres:
        :return:
        """
        # # 将返回的数据转为json数据
        # channelslists = json.loads(channelsres)
        # # 返回的数据是编码错误，则用下面代码解析数据
        # # channelslists = json.loads(json.dumps(channelsres,indent=4,ensure_ascii=False))
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            if k == "http://www.cpd.com.cn/app/xw/channels.json":
                channelList = json.loads(v)
                for channel in channelList['gd']:
                    channelid = channel['documents']
                    channelname = channel['cname']
                    channelparam = InitClass().channel_fields(channelid, channelname)
                    channelparams.append(channelparam)
                for channel in channelList['more']:
                    channelid = channel['documents']
                    channelname = channel['cname']
                    channelparam = InitClass().channel_fields(channelid, channelname)
                    channelparams.append(channelparam)
            elif k == "http://www.cpd.com.cn/app/hd/channels.json":
                channelList = json.loads(v)
                for channel in channelList['gd']:
                    channelid = channel['documents']
                    channelname = channel['cname']
                    channelparam = InitClass().channel_fields(channelid, channelname)
                    channelparams.append(channelparam)
                for channel in channelList['more']:
                    channelid = channel['documents']
                    channelname = channel['cname']
                    channelparam = InitClass().channel_fields(channelid, channelname)
                    channelparams.append(channelparam)
        spParam = InitClass().channel_fields('http://www.cpd.com.cn/app/yx/sp/documents.json', '影像-视频')
        channelparams.append(spParam)
        zbParam = InitClass().channel_fields('http://www.cpd.com.cn/app/yx/zb/documents.json', '影像-直播')
        channelparams.append(zbParam)
        mfyqParam = InitClass().channel_fields('http://www.cpd.com.cn/app/yq/mfyq/documents.json', '服务-资讯')
        channelparams.append(mfyqParam)
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
                "Host": "www.cpd.com.cn",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.8.0",
            }
            # 频道数据体
            # data = {}
            # 如果携带的是json数据体,用appjson发送
            # app_json = {}
            # 频道请求方式
            method = "get"
            # 若数据体以json形式发送则以下面方式发送数据上面方式注释
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname)
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
                for article in articlelist_json['top_datas']:
                    # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                    print(article)
                    articleparam = InitClass().article_list_fields()
                    articleparam = setArticleListParam(channelname, 1, articleparam, article);
                    articlesparams.append(articleparam)
                for article in articlelist_json['list_datas']:
                    # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                    print(article)
                    articleparam = InitClass().article_list_fields()
                    articleparam = setArticleListParam(channelname, 0, articleparam, article);
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
        # 频道请求头
        headers = {
            "Host": "www.cpd.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.0",
        }
        # 频道数据体
        # data = {}
        # 如果携带的是json数据体,用appjson发送
        # app_json = {}
        # 频道请求方式
        method = "get"
        for articleparam in articles:
            url = articleparam.get("channelid")
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
            article_show = InitClass().article_params_fields(url, headers, method, channelname, imgurl,
                                                             videourl=videos, videocover=videocover, pubtime=pubtime,
                                                             createtime=createtime, updatetime=updatetime,
                                                             source=source, author=author, likenum=likenum,
                                                             commentnum=commentnum, sharenum=sharenum, readnum=readnum,
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
            articleurl = articleres.get("articleurl")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["imageurl"] = imgurl
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
                fields["url"] = articleurl  # 文章的html网址，提取shareurl
                fields["workerid"] = articlejson['datas']['docid']  # 文章的id
                fields["title"] = articlejson['datas']['title']  # 文章的标题
                fields["content"] = articlejson['datas']['body']  # 文章的内容详情
                fields["articlecovers"] = articlejson['datas']['imgurl']  # 文章的封面，一般为上面get到的字段
                fields["images"] = articlejson['datas']['cimgs']  # 文章详情内的图片url，一般为列表需遍历获取
                fields["videos"] = articlejson['datas']['videourl']  # 文章的视频链接地址
                # fields["videocover"] = articlejson['data']['link']  # 文章的视频封面地址
                # fields["width"] = articlejson['data']['link']  # 文章的视频宽
                # fields["height"] = articlejson['data']['link']  # 文章的视频高
                fields["source"] = articlejson['datas']['source']  # 文章的来源
                fields["pubtime"] = articlejson['datas']['updatedate']  # 文章的发布时间
                # fields["createtime"] = articlejson['data']['pubDate']  # 文章的发布时间
                # fields["updatetime"] = articlejson['data']['pubDate']  # 文章的更新时间
                # fields["likenum"] = articlejson['data']['goodpost']  # 文章的点赞数
                # fields["playnum"] = articlejson['data']['link']  # 视频的播放数
                # fields["commentnum"] = len(articlejson['data']['comments'])  # 文章评论数
                # fields["readnum"] = articlejson['data']['click']  # 文章的阅读数
                # fields["trannum"] = articlejson['data']['link']  # 文章的转发数
                # fields["sharenum"] = articlejson['data']['link']  # 文章分享数
                # fields["author"] = articlejson['data']['author']  # 文章作者
                print(json.dumps(fields, indent=4, ensure_ascii=False))
            except Exception as e:
                print(e)

    def run(self):
        appParamsList = self.get_app_params().__next__()
        channelsres = {}
        for appParams in appParamsList:
            name = appParams['appurl']
            value = self.getchannels(appParams).__next__()
            channelsres[name] = value
        print(channelsres)
        channelsparams = self.analyzechannels(channelsres)
        articleparams = self.getarticlelistsparams(channelsparams.__next__())
        articles_ress = self.getarticlelists(articleparams.__next__())
        articles = self.analyze_articlelists(articles_ress.__next__())
        articlesparam = self.getarticleparams(articles.__next__())
        articles_html = self.getarticlehtml(articlesparam.__next__())
        self.analyzearticles(articles_html.__next__())


if __name__ == '__main__':
    spider = RenMinGongAnBao('人民公安报')
    spider.run()
