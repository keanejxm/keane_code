# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import time
from appspider_m import Appspider
from initclass import InitClass


class beijingshijianNews(Appspider):

    @staticmethod
    #从首页获取
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "https://app.api.btime.com/channel/getChannel"
        # 频道请求头
        headers = {
            'Host': 'app.api.btime.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.9.0',

        }
        # 频道数据体
        data = {
            'protocol':'4',
            'push_switch':'1',
            'token':'e0fb5784410cc184345a22632a803240',
            'carrier':'',
            'push_id':'5766a4b37307c04998dea233dcf9251f',
            'os_type':'Android',
            'timestamp':int(time.time()),
            'net':'WIFI',
            'os':'V417IR release-keys',
            'browse_mode':'1',
            'os_ver':'23',
            'sid':'',
            'location_citycode':'local_110000',
            'src':'lx_android',
            'channel':'xiaomi',
            'ver':'60301',
            'sign':"619a157",
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
        print(channelslists)
        channelparams = []
        for channel in channelslists['data']['like']:
            channelid = channel['cid']
            channelname = channel['cname']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)
        yield channelparams

    @staticmethod
    def getarticlelistsparams(channelsparams):
        """
        此方法目的是组建请求文章列页面数据参数，url，headers，data，若以json形式发送数据，则channeljson = channeljson
        :param channelsparams:
        :return:
        """
        url = "https://app.api.btime.com/news/list"
        method = 'get'
        headers = {
            'Host': 'app.api.btime.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.9.0',
        }
        articleparams = []
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            # 若有两个请求接口则如下： 例如：banner列表和文章列表时两个请求接口
            # url_banner = "http://cms.farmer.com.cn/api/app/front/content/list"  # banner请求接口

            data = {
                'protocol':'3',
                'cid':channelid,
                'cname':channelname,
                'is_paging':'1',
                'offset':'0',
                'refresh_type':'1',
                'refresh_count':'1',
                'last':'',
                'refresh_total':'1',
                'push_switch':'1',
                'token':'e0fb5784410cc184345a22632a803240',
                'carrier':'',
                'push_id':'5766a4b37307c04998dea233dcf9251f',
                'os_type':'Android',
                'timestamp':int(time.time()),
                'net':'WIFI',
                'os':'V417IR release-keys',
                'browse_mode':'1',
                'os_ver':'23',
                'sid':'',
                'location_citycode':'local_110000',
                'src':'lx_android',
                'channel':'xiaomi',
                'ver':'60301',
                'sign':'c778b0c',
            }
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
        for articleslist_res in articleslist_ress:
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
                    articlelists = articlelist_json['data']['data']
                    for article in articlelists:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        if articlelists.index(article) == 0 and article['module'] != 44:
                            if 'news' in article['data'].keys():
                                listdata = article['data']['news']
                                for articlecontent in listdata:
                                    print(article)
                                    articleparam = InitClass().article_list_fields()
                                    articleid = articlecontent['gid']
                                    articletitle = articlecontent['data']['title']
                                    try:
                                        articleparam["images"] = articlecontent['data']['covers']
                                    except Exception as e:
                                        print(f"在文章列表出无法获得封面图{e}")
                                    articleparam["articleid"] = articleid
                                    articleparam["articletitle"] = articletitle
                                    articleparam["channelname"] = channelname
                                    articleparam["channelid"] = channelid
                                    articleparam["banner"] = 1
                                    articlesparams.append(articleparam)
                            else:
                                print(article)
                                listdata = article['data']
                                articleparam = InitClass().article_list_fields()
                                articletitle = listdata['title']
                                try:
                                    articleparam["images"] = listdata['covers']
                                except Exception as e:
                                    print(f"在文章列表出无法获得封面图{e}")
                                articleparam["articleid"] = articleid
                                articleparam["articletitle"] = articletitle
                                articleparam["channelname"] = channelname
                                articleparam["channelid"] = channelid
                                articleparam["banner"] = 1
                                articlesparams.append(articleparam)
                        else:
                            articleid = article['gid']
                            if 'news' in article['data']:
                                listdata = article['data']['news']
                                for articlecontent in listdata:
                                    print(article)
                                    articleparam = InitClass().article_list_fields()
                                    articleid = articlecontent['gid']
                                    articletitle = articlecontent['data']['title']
                                    try:
                                        articleparam["images"] = articlecontent['data']['covers']
                                    except Exception as e:
                                        print(f"在文章列表出无法获得封面图{e}")
                                    articleparam["articleid"] = articleid
                                    articleparam["articletitle"] = articletitle
                                    articleparam["channelname"] = channelname
                                    articleparam["channelid"] = channelid
                                    articleparam["banner"] = 1
                                    articlesparams.append(articleparam)
                            else:
                                listdata = article['data']
                                articleparam = InitClass().article_list_fields()
                                articleid = article['gid']
                                articletitle = listdata['title']
                                try:
                                    articleparam["images"] = listdata['covers']
                                except Exception as e:
                                    print(f"在文章列表出无法获得封面图{e}")
                                articleparam["articleid"] = articleid
                                articleparam["articletitle"] = articletitle
                                articleparam["channelname"] = channelname
                                articleparam["channelid"] = channelid
                                articleparam["banner"] = 0
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
        url = 'https://app.api.btime.com/trans'
        headers = {
            'Content-Length': '0',
            'Host': 'app.api.btime.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.9.0',
        }
        method = 'post'
        for articleparam in articles:
            data = {
                'ver':'60301',
                'token':'e0fb5784410cc184345a22632a803240',
                'timestamp': int(time.time()),
                'src':'lx_android',
                'sign':'9a3a36c',
                'sid':'',
                'push_switch':'1',
                'push_id':'5766a4b37307c04998dea233dcf9251f',
                'protocol':'2',
                'os_ver':'23',
                'os_type':'Android',
                'os':'V417IR release-keys',
                'net':'WIFI',
                'm':'btime',
                'location_citycode':'local_110000',
                'gid': articleparam.get('articleid'),
                'fmt':'json',
                'channel':'xiaomi',
                'carrier':'',
                'browse_mode':'1',
            }
            if articleparam.get('articletype') == 3:
                url = 'https://app.api.btime.com/btv/relevant'
                method = 'get'
                headers = {
                    'Host': 'app.api.btime.com',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                    'User-Agent': 'okhttp/3.9.0',
                }
            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            channelid = articleparam.get("channelid")
            banner = articleparam.get("banner")
            imgurl = articleparam.get("images")
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
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data = data,
                                                        videourl = videos, videocover = videocover, pubtime = pubtime,
                                                        createtime = createtime, updatetime = updatetime,
                                                        source = source, author = author, likenum = channelid,
                                                        commentnum = commentnum, sharenum = sharenum, readnum = readnum,
                                                        articleurl = articleurl,banners = banner)
            articlesparam.append(article)
        yield articlesparam

    @staticmethod
    def analyzearticles(articles_res):
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            channelid = articleres.get("likenum")
            imgurl = articleres.get("images")
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
            fields["banner"] = banners
            # 如果有下列字段需添加
            # fields["url"] = articleurl #文章的html网址，提取shareurl
            # fields["workerid"] = workerid #文章的id
            # fields["title"] = title #文章的标题
            # fields["content"] = content #文章的内容详情
            # fields["articlecovers"] = imgurl #文章的封面，一般为上面get到的字段
            fields["images"] = imgurl #文章详情内的图片url，一般为列表需遍历获取
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
                # print(articlejson)
                htmlcoentent = ''
                if 'video' in articlejson['data'].keys():
                    if 'content' in articlejson['data'].keys():
                        for text in  articlejson['data']['content']:
                            if text['type'] == 'txt':
                                htmlcoentent += f"<p>{text['value']}</p>"
                            elif text['type'] == 'img':
                                htmlcoentent += f"<p><img src='{text['value']}' alt=''/><span></span></p>"

                            content = f"<div class='content'>{htmlcoentent}</div>"  # 文章内容
                    else:
                        content = ''
                    title = articlejson['data']['title']  # 标题
                    source = articlejson['data']['source']  # 来源
                    imgurl = articlejson['data']['image_urls']
                    pubtime = articlejson['data']['time']  # 发布时间
                    workerid = articlejson['data']['gid']
                    url = articlejson['data']["url"]
                    author = articlejson['data']["news_edit_user"]
                    if "comments" in articlejson['data'].keys():
                        commentnum = articlejson['data']["comments"]
                    else:
                        commentnum = '0'
                    videos = InitClass.get_video(content)
                    images = InitClass.get_images(content)
                    fields["videos"] = videos
                    fields["images"] = images
                    fields["appname"] = appname
                    fields["title"] = title
                    fields["url"] = url
                    fields["images"] = imgurl
                    fields["workerid"] = workerid
                    fields["source"] = source
                    fields["content"] = content
                    fields["author"] = author
                    fields["commentnum"] = commentnum
                    try:
                        fields["pubtime"] = int(pubtime)*1000
                    except Exception as e:
                        print(e)
                        fields["pubtime"] = int(pubtime)*1000
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
    spider = beijingshijianNews('北京时间')
    spider.run()
