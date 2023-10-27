# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
from urllib.parse import urlparse

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


class CaiZhengBu(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://app.mof.gov.cn/mofmobilenew/xinwen/channels_7972.json"
        # 频道请求头
        headers = {
            "Host": urlparse(url).netloc,
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.0",
        }
        method = "get"
        app_params = InitClass().app_params(url, headers, method)
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
        for channel in channelslists['model']:
            channelid = channel['channels']
            channelname = channel['cname']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)
        # channelid = channelslists['model'][5]['channels']
        # channelname = channelslists['model'][5]['cname']
        # channelparam = InitClass().channel_fields(channelid, channelname)
        # channelparams.append(channelparam)
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
                "Host": urlparse(url).netloc,
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.12.0",
            }
            method = 'get'
            # 若数据体以json形式发送则以下面方式发送数据上面方式注释
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname)
            articleparams.append(articlelist_param)
        yield articleparams

    @staticmethod
    def setarticlelistparam(channelname, banner, articleparam, article):
        if ('url' in article.keys() and article['url'].endswith(".json")) or \
                ('link' in article.keys() and article['link'].endswith(".json")):
            articleparam["channelname"] = channelname
            if 'url' in article.keys():
                articleparam["articleid"] = article['url']
            if 'link' in article.keys():
                articleparam["articleid"] = article['link']
            articleparam["articletitle"] = article['title']
            articleparam["banner"] = banner
            if 'cimgs' in article.keys() and len(article['cimgs']):
                articleparam["imageurl"] = article['cimgs'][0]
            if 'videourl' in article.keys():
                articleparam["videos"] = article['videourl']
            if 'pubDate' in article.keys():
                articleparam["pubtime"] = article['pubDate']
        return articleparam

    def analyze_articlelists(self, articleslist_ress):
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
                try:
                    if isinstance(articlelist_json, dict):
                        if 'top_text_datas' in articlelist_json.keys():
                            toptextdatas = articlelist_json['top_text_datas']
                            for article in toptextdatas:
                                articleparam = InitClass().article_list_fields()
                                articleparam = self.setarticlelistparam(channelname, 0, articleparam, article)
                                if articleparam['articleid']:
                                    articlesparams.append(articleparam)
                                else:
                                    print('网址新闻：', article)

                        if 'top_datas' in articlelist_json.keys():
                            topdatas = articlelist_json['top_datas']
                            for article in topdatas:
                                articleparam = InitClass().article_list_fields()
                                articleparam = self.setarticlelistparam(channelname, 1, articleparam, article)
                                if articleparam['articleid']:
                                    articlesparams.append(articleparam)
                                else:
                                    print('网址新闻：', article)

                        if 'top_datas_2' in articlelist_json.keys():
                            topdatas2 = articlelist_json['top_datas_2']
                            for article in topdatas2:
                                articleparam = InitClass().article_list_fields()
                                articleparam = self.setarticlelistparam(channelname, 0, articleparam, article)
                                if articleparam['articleid']:
                                    articlesparams.append(articleparam)
                                else:
                                    print('网址新闻：', article)

                        if 'list_datas' in articlelist_json.keys():
                            listdatas = articlelist_json['list_datas']
                            for article in listdatas:
                                articleparam = InitClass().article_list_fields()
                                articleparam = self.setarticlelistparam(channelname, 0, articleparam, article)
                                if articleparam['articleid']:
                                    articlesparams.append(articleparam)
                                else:
                                    print('网址新闻：', article)

                        if 'list_datas_2' in articlelist_json.keys():
                            listdatas2 = articlelist_json['list_datas_2']
                            for article in listdatas2:
                                articleparam = InitClass().article_list_fields()
                                articleparam = self.setarticlelistparam(channelname, 0, articleparam, article)
                                if articleparam['articleid']:
                                    articlesparams.append(articleparam)
                                else:
                                    print('网址新闻：', article)

                    elif isinstance(articlelist_json, list):
                        for article in articlelist_json:
                            articleparam = InitClass().article_list_fields()
                            articleparam = self.setarticlelistparam(channelname, 0, articleparam, article)
                            if articleparam['articleid']:
                                articlesparams.append(articleparam)
                            else:
                                print('网址新闻：', article)
                    else:
                        print("解析未识别:" + articlelist_json)

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

        method = 'get'
        for articleparam in articles:
            url_show = articleparam.get('articleid')
            headers = {
                "Host": urlparse(url_show).netloc,
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.12.0",
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
                                                             videourl = videos, videocover = videocover,
                                                             pubtime = pubtime,
                                                             createtime = createtime, updatetime = updatetime,
                                                             source = source, author = author, likenum = likenum,
                                                             commentnum = commentnum, sharenum = sharenum,
                                                             readnum = readnum,
                                                             articleid = articleid, articleurl = articleurl,
                                                             banners = banner)
            articlesparam.append(article_show)
        yield articlesparam

    @staticmethod
    def analyzearticles(articleresponsedata):
        for articleresponse in articleresponsedata:
            appname = articleresponse.get("appname")
            banner = articleresponse.get("banner")
            articleres = articleresponse.get("articleres")
            try:
                articlejson = eval(articleres)
                print(articlejson)
                fields = InitClass().article_fields()
                fields["appname"] = appname  # 应用名称，字符串
                fields["channelname"] = articlejson['datas']['cname']  # 频道名称，字符串
                fields["channelID"] = articlejson['datas']['cid']  # 频道id，字符串
                fields["channelType"] = ""  # 频道type，字符串
                fields["url"] = articlejson['datas']['sharelink']  # 分享的网址，字符串
                fields["workerid"] = articlejson['datas']['docid']  # 文章id，字符串
                fields["title"] = articlejson['datas']['title']  # 文章标题，字符串
                fields["content"] = articlejson['datas']['body']  # 文章内容，字符串
                fields["articlecovers"] = [] if not articlejson['datas']['imgurl'] else [
                    articlejson['datas']['imgurl']]  # 列表封面，数组
                fields["images"] = InitClass().get_images(fields["content"])  # 正文图片，数组
                if 'videourl' in articlejson['datas'].keys():
                    fields["videos"] = [] if not articlejson['datas']['videourl'] else [
                        articlejson['datas']['videourl']]  # 视频地址，数组
                fields["width"] = ""  # 视频宽，字符串
                fields["height"] = ""  # 视频高，字符串
                fields["source"] = ""  # 文章来源，字符串
                fields["pubtime"] = InitClass().date_time_stamp(
                    articlejson['datas']['updatedate'].replace("发布时间：", ""))  # 发布时间，时间戳（毫秒级，13位）
                fields["createtime"] = 0  # 创建时间，时间戳（毫秒级，13位）
                fields["updatetime"] = 0  # 更新时间，时间戳（毫秒级，13位）
                fields["likenum"] = 0  # 点赞数（喜欢数），数值
                fields["playnum"] = 0  # 播放数，数值
                fields["commentnum"] = 0  # 评论数，数值
                fields["readnum"] = 0  # 阅读数，数值
                fields["trannum"] = 0  # 转发数，数值
                fields["sharenum"] = 0  # 分享数，数值
                fields["author"] = ""  # 作者，字符串
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
    spider = CaiZhengBu('财政部')
    spider.run()
