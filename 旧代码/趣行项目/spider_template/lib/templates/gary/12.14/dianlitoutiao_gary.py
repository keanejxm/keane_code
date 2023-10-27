# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import bs4
import requests
import json
import re

from appspider_m import Appspider
from initclass import InitClass
"""
"articlecovers": "",   默认应为 []
"images": "",       默认应为 []
"videos": "",       默认应为 []
"videocover": "",       默认应为 []
"author": null,    默认为 ''
"pubtime": "2020-11-28"   时间类型不对 应为  160*************
"commentnum": null,  默认应为 0
"workerid": null,  这个 不应该为 null

"imageurl": [
        "https://api.chinapower.org.cn/public/images/29/1389886b090f4a007148a7841c1c42.png"
    ]  应该放入 images  
"""

class Yangshinews(Appspider):

    @staticmethod
    #从首页获取
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://api.chinapower.org.cn/index.php/index/index/allCategory"
        # 频道请求头
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'api.chinapower.org.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        # 频道数据体
        data = {}
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
        for channel in channelslists['info']:
            channelid = channel
            channelname = channel
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
        newsUrl = "http://api.chinapower.org.cn/index.php/index/index/selfNews?page=1"
        videoUrl = 'http://api.chinapower.org.cn/index.php/index/index/findModule?page=1'
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'api.chinapower.org.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        method = 'get'
        channelname="新闻"
        articlelist_param = InitClass().articlelists_params_fields(newsUrl, headers, method, channelname,)
        articlelist_param_video = InitClass().articlelists_params_fields(videoUrl, headers, method, channelname, )
        articleparams.append(articlelist_param)
        articleparams.append(articlelist_param_video)
        for channel in channelsparams:
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            index1 = channelsparams.index(channel)
            # 若有两个请求接口则如下： 例如：banner列表和文章列表时两个请求接口
            # url_banner = "http://cms.farmer.com.cn/api/app/front/content/list"  # banner请求接口
            url = "http://api.chinapower.org.cn/index.php/index/news/category"
            data = {
                'type': channelname,
                'page':	'1',
                'pagesize':	'20',
                'pull':	'down'
            }
            if index1 == 0:
                data = {
                    'type': channelname,
                    'page': '1',
                    'pagesize': '20',
                    'pull': 'down',
                    'top': '1'
                }
            # data_banner = {
            #     'orderBy': '4',
            #     'channelIds': channelid,
            #     'count': '4',
            #     'typeIds': '5',
            # }
            # articlelist_param_banner = InitClass().articlelists_params_fields(url_banner, headers, method, channelname,
            #                                                                   data = data_banner,
            #                                                                   banners = 1)  # 添加banner请求数据体，或其他接口请求数据
            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data, channelid = channelname)
            # 若数据体以json形式发送则以下面方式发送数据上面方式注释
            # articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data = data,channeljson = channeljson)
            # articleparams.append(articlelist_param_banner)
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
                    articlelists = articlelist_json['info']
                    for article in articlelists:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        if 'self_type' in article:
                            articleparam = InitClass().article_list_fields()
                            articletitle = article['self_title']
                            articleid = article['self_id']
                            videos = [article["self_thumbnail_url"]] #在此处获取到文章视频url，避免在文章详情获取不到视频链接，数据类型list
                            videocover = [article["videocover"]]#在此处获取到文章视频封面图，避免在文章详情获取不到视频封面图链接，数据类型list
                            articleparam["videos"] = videos
                            articleparam["videocover"] = videocover
                        else:
                            print(article)
                            articleparam = InitClass().article_list_fields()
                            articletitle = article['list_title']
                            articleid = article['list_id']
                            # videos = article["videourl"] #在此处获取到文章视频url，避免在文章详情获取不到视频链接，数据类型list
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
                            # articleparam["videocover"] = videocover#此步骤为存储视频封面
                            # articleparam["pubtime"] = pubtime#此步骤为存储发布时间
                            # articleparam["createtime"] = createtime#此步骤为存储创建时间
                            # articleparam["updatetime"] = updatetime#此步骤为存储更新时间
                            # articleparam["source"] = source#此步骤为存储文章来源
                            # articleparam["author"] = author#此步骤为存储作者
                            # articleparam["likenum"] = likenum#此步骤为存储点赞数
                            # articleparam["commentnum"] = commentnum#此步骤为存储评论数
                            try:
                                if 'images' in article:
                                    articleparam["images"] = article['images']
                                else:
                                    articleparam["images"] = [article['list_title_img_url']]
                            except Exception as e:
                                print(f"在文章列表出无法获得封面图{e}")
                        articleparam["articleid"] = articleid
                        articleparam["articletitle"] = articletitle
                        articleparam["channelname"] = channelname
                        articleparam["channelid"] = channelname
                        articleparam["banner"] = banners
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
        url = 'http://api.chinapower.org.cn/index.php/index/Import/collectStatus'
        headers = {
            'Host': 'api.chinapower.org.cn',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'UM_distinctid=1766eb1a9a863a-0c29bb703705da-c791e37-1fa400-1766eb1a9a914d; PHPSESSID=49fis0b9dqd0mov63q2ongo97g',
        }
        method = 'get'
        for articleparam in articles:
            data = {
                'list_id': articleparam.get("articleid"),
            }
            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            channelid = articleparam.get("channelname")
            banner = articleparam.get("banner")
            imgurl = articleparam.get("images")
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
                res = requests.get(articlejson['path'])
                res.encoding = res.apparent_encoding
                html = res.text
                bf = bs4.BeautifulSoup(html, 'html.parser')
                title = bf.find('h1').text
                source = bf.select('.avatar span')[0].text.replace('来源： ', '')
                pubtime = bf.select('.avatar span')[1].text.replace('时间：', '')
                content = bf.find('div',class_='text')
                title = title  # 标题
                source = source  # 来源
                content = str(content)  # 文章内容
                pubtime = pubtime  # 发布时间
                url = articlejson['path']
                if "author" in articlejson:
                    author = articlejson["author"]
                else:
                    author = ''
                if "workerid" in articlejson:
                    workerid = articlejson["workerid"]
                else:
                    workerid = re.compile(r'list_id=(\d+)')
                    workerid = workerid.findall(articlejson['path'])[0]
                if "commentnum" in articlejson:
                    commentnum = articlejson["commentnum"]
                else:
                    commentnum = 0
                videos = InitClass.get_video(content)
                images = InitClass.get_images(content)
                fields["appname"] = appname
                fields["title"] = title
                fields["url"] = url
                fields["workerid"] = workerid
                fields["source"] = source
                fields["content"] = content
                fields["author"] = author
                fields["commentnum"] = commentnum
                fields["images"] = images
                fields["videos"] = videos
                fields["channelID"] = channelname
                fields["pubtime"] = InitClass().date_time_stamp(InitClass().format_date(pubtime))
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
    spider = Yangshinews('电力头条')
    spider.run()
