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
"commentnum": null,   默认为 ''
"content": null,  正文提取失败
"""
import json

from appspider_m import Appspider
from initclass import InitClass


class jiaohuidian(Appspider):

    @staticmethod
    #从首页获取
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "https://jarticle.xhby.net/v3/api/columns"
        # 频道请求头
        headers = {
            "accept": "application/json",
            "cache-control": "no-cache",
            "authorization": "Bearer null",
            "Host": "jarticle.xhby.net",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Cookie": "acw_tc=76b20f7016081070463235460e7242ba8bbfeee598dc2fdaaa7c8ffd0899dd; SERVERID=594b3f5153c1147b39af6db84ed83aab|1608107116|1608104806",
            "User-Agent": "okhttp/3.12.1"
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
        for channel in channelslists['data']['column']:
            channelid = channel['id']
            channelname = channel['title']
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
        articleparams = []
        # videourl = "https://jarticle.xhby.net/v3/api/getColumnArticle"
        # videoheaders = {
        #     "accept": 'application/json',
        #     'cache-control': 'no-cache',
        #     'authorization': 'Bearer null',
        #     'Host': 'jarticle.xhby.net',
        #     'Connection': 'Keep-Alive',
        #     'Accept-Encoding': 'gzip',
        #     'Cookie': 'acw_tc=76b20f6016081669830524795e22ceb328b2ae66683266aeb4a369d5601bb7; SERVERID=594b3f5153c1147b39af6db84ed83aab|1608166986|1608166983',
        #     "User-Agent": "okhttp/3.12.1"
        # }
        # videodata = {
        #     'column_id': '8892fc81fbea47ff9447d5889d1b9c2a',
        #     'page': '10',
        #     'updateCID': '635c485bc510fde',
        #     'hide_top': '0',
        # }
        # method = 'get'
        # channelname = "视频"
        # articlelist_param = InitClass().articlelists_params_fields(videourl, videoheaders, method, channelname, data=videodata)
        # articleparams.append(articlelist_param)
        for index in range(0,3):
            liveurl = f"https://jarticle.xhby.net/v3/api/new_live_articles/{index+1}"
            liveheaders = {
                "accept": 'application/json',
                'cache-control': 'no-cache',
                'authorization': 'Bearer null',
                'Host': 'jarticle.xhby.net',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
                'Cookie': 'acw_tc=76b20f6016081669830524795e22ceb328b2ae66683266aeb4a369d5601bb7; SERVERID=594b3f5153c1147b39af6db84ed83aab|1608166986|1608166983',
                "User-Agent": "okhttp/3.12.1"
            }
            livedata = {
                'page': '1',
                'limt': "10"
            }
            method = 'get'
            channelname = "直播"
            articlelist_param = InitClass().articlelists_params_fields(liveurl, liveheaders, method, channelname, channelid=channelname,
                                                                       data=livedata)
            articleparams.append(articlelist_param)
        # for channel in channelsparams:
        #     channelid = channel.get("channelid")
        #     channelname = channel.get("channelname")
        #     # 若有两个请求接口则如下： 例如：banner列表和文章列表时两个请求接口
        #     # url_banner = "http://cms.farmer.com.cn/api/app/front/content/list"  # banner请求接口
        #     url = "https://jarticle.xhby.net/v3/api/getColumnArticle"
        #     headers = {
        #         "accept": 'application/json',
        #         'cache-control': 'no-cache',
        #         'authorization':'Bearer null',
        #         'Host': 'jarticle.xhby.net',
        #         'Connection': 'Keep-Alive',
        #         'Accept-Encoding': 'gzip',
        #         'Cookie': 'acw_tc=76b20f7016081070463235460e7242ba8bbfeee598dc2fdaaa7c8ffd0899dd; SERVERID=594b3f5153c1147b39af6db84ed83aab|1608107759|1608104806',
        #         "User-Agent": "okhttp/3.12.1"
        #     }
        #     data = {
        #         'column_id':channelid,
        #         'page':'10',
        #         'updateCID':'635c485bc510fde',
        #         'hide_top':'0',
        #     }
        #     method = 'get'
        #     articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data)
        #     # 若数据体以json形式发送则以下面方式发送数据上面方式注释
        #     # articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,channeljson = channeljson)
        #     # articleparams.append(articlelist_param_banner)
        #     #获取视频
        #     articleparams.append(articlelist_param)
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
                #若banner图在articlelist_json中则分来开取并给其复制banner = 1
                try:
                    if "article_top" in articlelist_json['data'].keys() or 'article' in articlelist_json['data'].keys() or 'data' in articlelist_json['data'].keys():
                        if "article_top" in articlelist_json['data'].keys():
                            articlelists = articlelist_json['data']['article_top']
                            print(articlelist_json)
                            print(articlelists)
                            if 'report_articles' in articlelists:
                                articlelists = articlelists['report_articles']
                            for article in articlelists:
                                articleparam = InitClass().article_list_fields()
                                articletitle = article['title']
                                articleid = article['id']
                                try:
                                    if 'pic3' in article:
                                        articleparam["images"] = [article['pic3']]
                                    elif 'pic2' in article:
                                        articleparam["images"] = [article['pic2']]
                                    else:
                                        articleparam["images"] = []
                                except Exception as e:
                                    print(f"在文章列表出无法获得封面图{e}")
                                articleparam["articleid"] = articleid
                                articleparam["articletitle"] = articletitle
                                articleparam["channelname"] = channelname
                                articleparam["banner"] = banners
                                articlesparams.append(articleparam)
                        elif "data" in articlelist_json['data']:
                            articlelists = articlelist_json['data']['data']
                            if 'report_articles' in articlelists:
                                articlelists = articlelists['report_articles']
                            for article in articlelists:
                                articleparam = InitClass().article_list_fields()
                                articletitle = article['title']
                                articleid = article['id']
                                channelid = article['column_id']
                                if 'start_time' in article:
                                    start_time = article['start_time']
                                else:
                                    start_time = ''
                                try:
                                    if 'pic3' in article:
                                        articleparam["images"] = [article['pic3']]
                                    elif 'pic2' in article:
                                        articleparam["images"] = [article['pic2']]
                                    else:
                                        articleparam["images"] = None
                                except Exception as e:
                                    print(f"在文章列表出无法获得封面图{e}")
                                articleparam["articleid"] = articleid
                                articleparam["articletitle"] = articletitle
                                articleparam["channelname"] = channelname
                                articleparam["banner"] = banners
                                articleparam['channelid']=channelid
                                articleparam['start_time'] = start_time
                                articlesparams.append(articleparam)
                        else:
                            articlelists = articlelist_json['data']['article']
                            for article in articlelists['data']:
                                # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                                print(article)
                                articleparam = InitClass().article_list_fields()
                                articletitle = article['title']
                                articleid = article['id']
                                videos = [article['video_url']] #在此处获取到文章视频url，避免在文章详情获取不到视频链接，数据类型list
                                # videocover = article["videocover"]#在此处获取到文章视频封面图，避免在文章详情获取不到视频封面图链接，数据类型list
                                # pubtime = article["pubtime"]#在此处获取到文章的发布时间，避免在文章详情获取不到发布时间
                                # createtime = article["createtime"]#在此处获取到文章的创建时间，避免在文章详情获取不创建时间
                                # updatetime = article["updatetime"]#在此处获取到文章的更新时间，避免在文章详情获取不到更新时间
                                # source = article["source"]#在此处获取到文章的来源，避免在文章详情获取不到来源
                                # author = article["author"]#在此处获取到文章的作者，避免在文章详情获取不到作者
                                # likenum = article["likenum"]#在此处获取到文章的点赞数，避免在文章详情获取不到点赞数
                                # commentnum = article["commentnum"]#在此处获取到文章的评论数，避免在文章详情获取不到评论数
                                # sharenum = article["sharenum"]#在此处获取到文章的评论数，避免在文章详情获取不到评论数
                                # readnum = article["readnum"]#在此处获取到文章的阅读数，避免在文章详情获取不到阅读数
                                # articleurl = article["articleurl"]#在此处获取到文章html地址，避免在文章详情获取不到html地址
                                # articleparam["video"] = videos #此步骤为存储视频url
                                # articleparam["videocover"] = []#此步骤为存储视频封面
                                # articleparam["pubtime"] = pubtime#此步骤为存储发布时间
                                # articleparam["createtime"] = createtime#此步骤为存储创建时间
                                # articleparam["updatetime"] = updatetime#此步骤为存储更新时间
                                # articleparam["source"] = source#此步骤为存储文章来源
                                # articleparam["author"] = author#此步骤为存储作者
                                # articleparam["likenum"] = likenum#此步骤为存储点赞数
                                # articleparam["commentnum"] = commentnum#此步骤为存储评论数
                                try:
                                    if 'pic3' in article:
                                        articleparam["images"] = [article['pic3']]
                                    elif 'pic2' in article :
                                        articleparam["images"] = [article['pic2']]
                                    else:
                                        articleparam["images"] = None
                                except Exception as e:
                                    print(f"在文章列表出无法获得封面图{e}")
                                articleparam["articleid"] = articleid
                                articleparam["articletitle"] = articletitle
                                articleparam["channelname"] = channelname
                                articleparam["banner"] = banners
                                articleparam["videos"] = videos
                                articleparam["channelid"] = channelid
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
        print(articles)
        articlesparam = []
        headers = {
            'accept': 'application/json',
            'cache-control': 'no-cache',
            'authorization': 'Bearer null',
            'Host': 'japi.xhby.net',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Cookie': 'SERVERID=594b3f5153c1147b39af6db84ed83aab|1608110012|1608104796',
            'User-Agent': 'okhttp/3.12.1',
        }
        method = 'get'
        for articleparam in articles:
            if articleparam.get('channelid') != '' and articleparam.get('start_time') != '':
                url = f'https://japi.xhby.net/v3/api/getArticleInfo/{articleparam.get("articleid")}?columnId={articleparam.get("channelid")}'
            elif articleparam.get('channelid') != '' and articleparam.get('start_time') == '':
                url = f'https://japi.xhby.net/v3/api/live_info/{articleparam.get("articleid")}?type=1'
            else:
                url = f'https://japi.xhby.net/v3/api/getArticleInfo/{articleparam.get("articleid")} '
            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
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
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl,
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
            imgurl = articleres.get("imageurl")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            # 若上面存储了此字段需用下列方式获取
            # videos = articleres.get("videos")
            videocover = imgurl
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
            fields["images"] = imgurl
            fields["banner"] = banners
            # 如果有下列字段需添加
            # fields["url"] = articleurl #文章的html网址，提取shareurl
            # fields["workerid"] = workerid #文章的id
            # fields["title"] = title #文章的标题
            # fields["content"] = content #文章的内容详情
            fields["articlecovers"] = imgurl #文章的封面，一般为上面get到的字段
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
                print(articlejson)
                if 'article' in articlejson['data']:
                    title = articlejson['data']['article']['title']  # 标题
                    if 'source' in articlejson['data']['article'].keys():
                        source = articlejson['data']['article']['source']  # 来源
                    else:
                        source= ''
                    content = articlejson['data']['article']['content']  # 文章内容
                    pubtime = articlejson['data']['article']['created_at']  # 发布时间
                    workerid = articlejson['data']['article']['id']
                    url = articlejson['data']['article']["shareUrl"]
                    author = articlejson['data']['article']['aEditor']
                    if "comments" in articlejson['data']['article']:
                        commentnum = articlejson['data']['article']["comments"]
                    else:
                        commentnum = ''
                else:
                    if len(articlejson['data']['discusses'])>0:
                        title = articlejson['data']['discusses'][0]['title']  # 标题
                        if 'source' in articlejson['data']['discusses'][0].keys():
                            source = articlejson['data']['discusses'][0]['source']  # 来源
                        else:
                            source= ''
                        content = articlejson['data']['discusses'][0]['content']  # 文章内容
                        pubtime = articlejson['data']['discusses'][0]['updateTime']  # 发布时间
                        workerid = articlejson['data']['discusses'][0]['id']
                        url = ''
                        author = articlejson['data']['discusses'][0]['audit']
                        if "comments" in articlejson['data']['discusses'][0]:
                            commentnum = articlejson['data']['discusses'][0]["comments"]
                        else:
                            commentnum = ''
                fields["appname"] = appname
                fields["title"] = title
                fields["url"] = url
                fields["workerid"] = workerid
                fields["source"] = source
                fields["content"] = content
                fields["author"] = author
                fields['channelID'] = channelname
                fields["commentnum"] = commentnum
                fields["pubtime"] = InitClass().date_time_stamp(pubtime)
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
    spider = jiaohuidian('交汇点新闻')
    spider.run()
