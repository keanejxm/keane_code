# Author jovan
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import bs4
import requests

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass

#运行不通
class DongBeiTouTiao(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道请求头
        headers = {
            "Host": "dfzdbapi.eastday.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.8.1",
        }
        method = "get"
        # 频道url
        url1 = "http://dfzdbapi.eastday.com/api/Channel/List"
        url2 = "http://dfzdbapi.eastday.com/api/Channel/VideoList"
        app_params1 = InitClass().app_params(url1, headers, method)
        app_params2 = InitClass().app_params(url2, headers, method)
        yield [app_params1, app_params2]

    @staticmethod
    def analyzechannels(channelsres):
        """
        此方法主要获取channelid,channelname即可
        若请求文章列表页需要channeltype，categoryname，categoryid,则以categoryname= categoryname形式传递参数
        :param channelsres:
        :return:
        """
        print(channelsres)
        channelparams = []
        for k, v in channelsres.items():
            channellist = json.loads(v)
            for channel in channellist['list']:
                channelid = channel['channelId']
                channelname = channel['title']
                channeltype = channel['channelType']
                categoryid = channel['url']
                channelparam = InitClass().channel_fields(channelid, channelname, channeltype = channeltype,
                                                          categoryid = categoryid)
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
            categoryid = channel.get("categoryid")
            url = f"http://dfzdbapi.eastday.com{categoryid}"
            headers = {
                "Content-Type": "application/json;charset=UTF-8",
                "Content-Length": "135",
                "Host": "dfzdbapi.eastday.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.8.1",
                "Cache-Control": "no-cache",
            }
            method = 'post'
            # 如果携带的是json数据体,用appjson发送
            channel_json = {
                "newsType": "0",
                "deviceId": "08002741B1E0",
                "appId": "DBTT-Android",
                "channelId": channelid,
                "currentPage": "1",
                "version": "V2.5.6",
                "pageSize": "20"
            }
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname,
                                                                       channeljson = channel_json)
            articleparams.append(articlelist_param)
        yield articleparams

    @staticmethod
    def setarticlelistparam(channelname, banner, articleparam, article):
        articleparam["channelid"] = article['channelId']
        articleparam["channelname"] = channelname
        articleparam["articleid"] = article['newsId']
        articleparam["articletype"] = article['newsType']
        articleparam["articletitle"] = article['title']
        articleparam["banner"] = banner
        if len(article['imgUrls']):
            articleparam["imageurl"] = article['imgUrls']
        articleparam["articleurl"] = article['url']
        articleparam["videos"] = article['videoUrl']
        if article['newsType'] == 2:
            articleparam["videocover"] = article['imgUrls'][0]
        articleparam["pubtime"] = article['time']
        if 'duration' in article.keys():
            articleparam["createtime"] = article['duration']  # 暂存视频时长
        if 'videoSize' in article.keys():
            articleparam["updatetime"] = article['videoSize']  # 暂存视频大小
        articleparam["source"] = article['infoSource']
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
                if 'list' in articlelist_json.keys() and isinstance(articlelist_json['list'], list):
                    for article in articlelist_json['list']:
                        articleparam = InitClass().article_list_fields()
                        articleparam = self.setarticlelistparam(channelname, 0, articleparam, article)
                        articlesparams.append(articleparam)
                if 'banners' in articlelist_json.keys() and isinstance(articlelist_json['banners'], list):
                    for article in articlelist_json['banners']:
                        articleparam = InitClass().article_list_fields()
                        articleparam = self.setarticlelistparam(channelname, 1, articleparam, article)
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

        method = 'get'
        for articleparam in articles:
            # url_show = ""
            url_show = articleparam.get('articleurl')
            headers = {
                "Host": "dfzdbapi.eastday.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.8.1",
            }
            articletitle = articleparam.get("articletitle")
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
            commentnum = articleparam.get("commentnum")
            sharenum = articleparam.get("sharenum")
            readnum = articleparam.get("readnum")
            articleurl = articleparam.get("articleurl")
            # 若APP有关于时间的反爬加sleeptime = 1，若发送为json数据体，则添加articlejson = articlejson
            # 这里url_show传的获取详情网页地址，但是会乱码，所以在下个方法再次请求详情
            article_show = InitClass().article_params_fields(url_show, headers, method, channelname, imgurl,
                                                             videourl = videos, videocover = videocover,
                                                             pubtime = pubtime,
                                                             createtime = createtime, updatetime = updatetime,
                                                             source = source, author = author, likenum = articletitle,
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
            channelname = articleresponse.get("channelname")
            imageurl = articleresponse.get("imageurl")
            videourl = articleresponse.get("videourl")
            videocover = articleresponse.get("videocover")
            articleurl = articleresponse.get("articleurl")
            articleid = articleresponse.get("articleid")
            pubtime = articleresponse.get("pubtime")
            source = articleresponse.get("source")
            author = articleresponse.get("author")
            title = articleresponse.get("likenum")  # 使用暂存标题
            readnum = articleresponse.get("readnum")
            sharenum = articleresponse.get("sharenum")
            commentnum = articleresponse.get("commentnum")
            banner = articleresponse.get("banner")

            try:
                print(articleresponse)
                res = requests.get(articleurl)
                res.encoding = res.apparent_encoding
                html = res.text
                bf = bs4.BeautifulSoup(html, 'html.parser')
                content = bf.find('div', class_ = 'content').prettify()

                fields = InitClass().article_fields()
                fields["appname"] = appname  # 应用名称，字符串
                fields["channelname"] = channelname  # 频道名称，字符串
                fields["channelID"] = ""  # 频道id，字符串
                fields["channelType"] = ""  # 频道type，字符串
                fields["url"] = articleurl  # 分享的网址，字符串
                fields["workerid"] = articleid  # 文章id，字符串
                fields["title"] = title  # 文章标题，字符串
                fields["content"] = content  # 文章内容，字符串
                fields["articlecovers"] = imageurl  # 列表封面，数组
                fields["images"] = InitClass().get_images(fields["content"])  # 正文图片，数组
                fields["videos"] = [] if not videourl else [videourl]  # 视频地址，数组
                fields["videocover"] = [] if not videocover else [videocover]  # 视频封面，数组
                fields["width"] = ""  # 视频宽，字符串
                fields["height"] = ""  # 视频高，字符串
                fields["source"] = source  # 文章来源，字符串
                fields["pubtime"] = InitClass().date_time_stamp(pubtime)  # 发布时间，时间戳（毫秒级，13位）
                fields["createtime"] = 0  # 创建时间，时间戳（毫秒级，13位）
                fields["updatetime"] = 0  # 更新时间，时间戳（毫秒级，13位）
                fields["likenum"] = 0  # 点赞数（喜欢数），数值
                fields["playnum"] = 0  # 播放数，数值
                fields["commentnum"] = commentnum  # 评论数，数值
                fields["readnum"] = readnum  # 阅读数，数值
                fields["trannum"] = 0  # 转发数，数值
                fields["sharenum"] = sharenum  # 分享数，数值
                fields["author"] = author  # 作者，字符串
                fields["banner"] = banner  # banner标记，数值（0标识不是，1标识是）
                fields["specialtopic"] = 0  # 是否是专题，数值（0标识不是，1标识是）
                fields["topicid"] = ""  # 专题id，字符串

                print(json.dumps(fields, indent = 4, ensure_ascii = False))
            except Exception as e:
                print(e)

    def run(self):
        appParamsList = self.get_app_params().__next__()
        channelsres = {}
        for appParams in appParamsList:
            name = appParams['appurl']
            value = self.getchannels(appParams).__next__()
            channelsres[name] = value
        channelsparams = self.analyzechannels(channelsres)
        articleparams = self.getarticlelistsparams(channelsparams.__next__())
        articles_ress = self.getarticlelists(articleparams.__next__())
        articles = self.analyze_articlelists(articles_ress.__next__())
        articlesparam = self.getarticleparams(articles.__next__())
        articles_html = self.getarticlehtml(articlesparam.__next__())
        self.analyzearticles(articles_html.__next__())


if __name__ == '__main__':
    spider = DongBeiTouTiao('东北头条')
    spider.run()
