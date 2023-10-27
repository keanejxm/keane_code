# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
"""
"articlecovers": "",   默认应为 []
"images": "",       默认应为 []
"videos": "",       默认应为 []
"videocover": "",       默认应为 []
"imageurl": [
        "http://rmrbpre.img-cn-beijing.aliyuncs.com/zgrd/dir2/20190212/zgrd_10_20181236c7aba2-a242-4cbb-92a2-79d2a9cfd0be.jpg"
    ] 值应该给 images
"pubtime": "2019-02-12T12:49:42+0800", 时间应装换为时间戳 ...
"""
import json

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


class Quanguorendanews(Appspider):

    @staticmethod
    #从首页获取
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://rdapi.peopletech.cn/api/v2/menus/"
        # 频道请求头
        headers = {
            "Content-Type": "application/json",
            "Host": "rdapi.peopletech.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
        }
        # 频道数据体
        data = {
            "platform":"android",
            "clientVersionCode": "15",
            "deviceOs": "6.0.1",
            "pjCode":"zgrd_10_201812",
            "device_size":"810.0x1440.0",
            "clientVersion":"2.1.4",
            "deviceModel": "Netease-MuMu",
            "udid": "010000000308435",
            "channel": "xiaomi",
        }
        # 如果携带的是json数据体,用appjson发送
        # app_json = {}
        # 频道请求方式
        method = "get"
        app_params = InitClass().app_params(url, headers, method, data = data)
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
        channelparams = []
        for channel in channelslists['items']:
            print(channel)
            channelid = channel['categoryId']
            categoryid = channel['id']
            channelname = channel['name']
            if 'children' in channel.keys():
                categorychild = channel['children']
                channelparam = InitClass().channel_fields(channelid, channelname, categoryid = categoryid, categoryname = categorychild)
                channelparams.append(channelparam)
            else:
                channelparam = InitClass().channel_fields(channelid, channelname, categoryid= categoryid)
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
        print(channelsparams)
        for channel in channelsparams:
            print(channel)
            headers = {
                "Content-Type": "application/json",
                "Host": "rdapi.peopletech.cn",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
            }
            data = {
                "pageToken":"",
                "size":"20",
                "platform":"android",
                "clientVersionCode": "15",
                "deviceOs": "6.0.1",
                "pjCode":"zgrd_10_201812",
                "device_size":"810.0x1440.0",
                "clientVersion":"2.1.4",
                "deviceModel": "Netease-MuMu",
                "udid": "010000000308435",
                "channel": "xiaomi",
            }
            method = 'get'
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            categoryid = channel.get('categoryid')
            if 'categorychild' in channel.keys() and len(channel.get('categorychild')):
                for children in channel.get('categorychild'):
                    channelid = children.get("categoryId")
                    channelname = children.get("name")
                    url = f"https://rdapi.peopletech.cn/api/v2/articles/{channelid}?"
                    articlelist_param_children = InitClass().articlelists_params_fields(url, headers, method, channelname,channelid = channelid,
                                                                               data=data)
                    articleparams.append(articlelist_param_children)
            # 若有两个请求接口则如下： 例如：banner列表和文章列表时两个请求接口
            # url_banner = f"https://rdapi.peopletech.cn/api/v2/articles/{channelid}"# banner请求接口
            url = f"https://rdapi.peopletech.cn/api/v2/articles/{channelid}?"
            #     articlelist_param_banner = InitClass().articlelists_params_fields(url_banner, headers, method, channelname,
            #                                                                   data = data,
            #                                                                   banners = 1)  # 添加banner请求数据体，或其他接口请求数据
            #     articleparams.append(articlelist_param_banner)
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,channelid = channelid)
            # 若数据体以json形式发送则以下面方式发送数据上面方式注释
            # articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,channeljson = channeljson)
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
        print(articleslist_ress)
        for articleslist_res in articleslist_ress:
            print(articleslist_res)
            banners = articleslist_res.get("banner")
            channelname = articleslist_res.get("channelname")
            channelid = articleslist_res.get("channelid")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                # 可在下面打印处打断点，查看请求到的数据
                print(articlelist_json)
                #若banner图在articlelist_json中则分来开取并给其复制banner = 1
                try:
                    articlelists = articlelist_json['item']['list']
                    for article in articlelists:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        print(article)
                        articleparam = InitClass().article_list_fields()
                        articletitle = article['title']
                        articleid = article['articleId']
                        # videos = article["videourl"] #在此处获取到文章视频url，避免在文章详情获取不到视频链接，数据类型list
                        # videocover = article["videocover"]#在此处获取到文章视频封面图，避免在文章详情获取不到视频封面图链接，数据类型list
                        # pubtime = article["pubtime"]#在此处获取到文章的发布时间，避免在文章详情获取不到发布时间
                        # createtime = article["createtime"]#在此处获取到文章的创建时间，避免在文章详情获取不创建时间
                        updatetime = article["date"]#在此处获取到文章的更新时间，避免在文章详情获取不到更新时间
                        # source = article["source"]#在此处获取到文章的来源，避免在文章详情获取不到来源
                        # author = article["author"]#在此处获取到文章的作者，避免在文章详情获取不到作者
                        # likenum = article["likenum"]#在此处获取到文章的点赞数，避免在文章详情获取不到点赞数
                        # commentnum = article["commentnum"]#在此处获取到文章的评论数，避免在文章详情获取不到评论数
                        # sharenum = article["sharenum"]#在此处获取到文章的评论数，避免在文章详情获取不到评论数
                        # readnum = article["readnum"]#在此处获取到文章的阅读数，避免在文章详情获取不到阅读数
                        # articleurl = article["articleurl"]#在此处获取到文章html地址，避免在文章详情获取不到html地址
                        # articleparam["video"] = videos #此步骤为存储视频url
                        # articleparam["videocover"] = videocover#此步骤为存储视频封面
                        # articleparam["pubtime"] = pubtime#此步骤为存储发布时间
                        # articleparam["createtime"] = createtime#此步骤为存储创建时间
                        # articleparam["updatetime"] = updatetime#此步骤为存储更新时间
                        # articleparam["source"] = source#此步骤为存储文章来源
                        # articleparam["author"] = author#此步骤为存储作者
                        # articleparam["likenum"] = likenum#此步骤为存储点赞数
                        # articleparam["commentnum"] = commentnum#此步骤为存储评论数
                        try:
                            if "images" in article:
                                articleparam["images"] = article['images']
                            else:
                                articleparam["images"] = []
                        except Exception as e:
                            print(f"在文章列表出无法获得封面图{e}")
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["channelname"] = channelname
                        articleparam["channelid"] = channelid
                        articleparam["updatetime"] = updatetime
                        articlesparams.append(articleparam)
                        print(articlesparams)
                    if 'head' in articlelist_json['item']:
                        articlebanner = articlelist_json['item']['head']
                        for article in articlebanner:
                            articleparam = InitClass().article_list_fields()
                            articletitle = article['title']
                            articleid = article['articleId']
                            updatetime = article["date"]
                            banner = 1
                            try:
                                articleparam["images"] = [article['images']]
                            except Exception as e:
                                print(f"在文章列表出无法获得封面图{e}")
                            articleparam["articleid"] = articleid
                            articleparam["articletitle"] = articletitle
                            articleparam["channelname"] = channelname
                            articleparam["channelid"] = channelid
                            articleparam["updatetime"] = updatetime
                            articleparam["banner"] = banner
                            print(articlesparams)
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
        headers = {
            "Content-Type": "application/json",
            "Host": "rdapi.peopletech.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36",
        }
        method = 'get'
        for articleparam in articles:
            articleid = articleparam.get('articleid')
            url = f'https://rdapi.peopletech.cn/api/v2/articles/detail/{articleid}'
            data = {
                "platform":"android",
                "clientVersionCode": "15",
                "deviceOs": "6.0.1",
                "pjCode":"zgrd_10_201812",
                "device_size":"810.0x1440.0",
                "clientVersion":"2.1.4",
                "deviceModel": "Netease-MuMu",
                "udid": "010000000308435",
                "channel": "xiaomi",
            }
            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            likenum = articleparam.get("channelid")
            banner = articleparam.get("banner")
            imgurl = articleparam.get("images")
            videos = []
            videocover = []
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
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data = data,
                                                        videourl = videos, videocover = videocover, pubtime = pubtime,
                                                        createtime = createtime, updatetime = updatetime,
                                                        source = source, author = author, likenum = likenum,
                                                        commentnum = commentnum, sharenum = sharenum, readnum = readnum,
                                                        articleurl = articleurl,banners = banner)
            articlesparam.append(article)
        yield articlesparam

    @staticmethod
    def analyzearticles(articles_res):
        for articleres in articles_res:
            print(articleres)
            channelname = articleres.get("channelname")
            channelid = articleres.get("likenum")
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
            # articleurl = articleres.get("articleurl")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["channelID"] = channelid
            fields["images"] = imgurl
            fields["banner"] = banners
            # 如果有下列字段需添加
            # fields["url"] = articleurl #文章的html网址，提取shareurl
            # fields["workerid"] = workerid #文章的id
            # fields["title"] = title #文章的标题
            # fields["content"] = content #文章的内容详情
            fields["articlecovers"] = [] #文章的封面，一般为上面get到的字段
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
                articlejson = json.loads(json.dumps(json.loads(articleres), indent = 4, ensure_ascii = False))
                if 'item' in articlejson:
                    print(articlejson)
                    title = articlejson['item']['title']  # 标题
                    if "source" in articlejson['item']:
                        source = articlejson['item']["source"]
                    else:
                        source = ''
                    if "content" in articlejson['item']:
                        content = articlejson['item']["content"]
                    else:
                        content = ''
                    videos = InitClass.get_video(content)
                    images = InitClass.get_video(content)
                    pubtime = articlejson['item']['date']  # 发布时间
                    workerid = articlejson['item']['id']
                    url = articlejson['item']["shareUrl"]
                    if "author" in articlejson['item']:
                        author = articlejson['item']["author"]
                    else:
                        author = None
                    commentnum = articlejson['item']["comments"]
                    fields["appname"] = appname
                    fields["title"] = title
                    fields["url"] = url
                    fields["workerid"] = workerid
                    fields["source"] = source
                    fields["content"] = content
                    fields["videos"] = videos
                    fields["images"] = images
                    fields["author"] = author
                    fields["commentnum"] = commentnum
                    fields["pubtime"] = InitClass().date_time_stamp(InitClass().format_date(pubtime))*1000
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
    spider = Quanguorendanews('全国人大')
    spider.run()
