# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json
import urllib.parse
import logging
from app_templates.lib.templates.appspider_m import Appspider
from app_templates.lib.templates.initclass import InitClass


def setArticleListParam(channelname, banner, articleparam, article):
    if 'itemUrl' in article.keys() and article['itemUrl'] != '':
        articleparam["articleurl"] = article['itemUrl']
    elif 'itemId' in article.keys():
        if article['itemId'].endswith('.json'):
            articleparam["articleid"] = urllib.parse.unquote(article['itemId'])
        elif article['itemId'].startswith('ART'):
            articleparam["articleid"] = 'https://api.app.cctv.com/api/article/' + article['itemId']
        elif article['itemId'].startswith('PHO'):
            articleparam["articleid"] = 'https://api.app.cctv.com/api/album/' + article['itemId']
        elif article['itemId'].startswith('VSET') or article['itemId'] != "":
            if article['playid'] == '':
                articleparam["articleid"] = "https://api.app.cctv.com/api/getVideoPageDetail?videoSetContentId=" + \
                                            article['itemId']
            else:
                # articleparam["articleid"] = "https://api.app.cctv.com/api/getVideoPageDetail?videoGuid=" + \
                #                             article['playid'] + "&"
                articleparam["articleid"] = 'https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid=' + article[
                    'playid'] + '&client=androidapp&tsp=1607594618&vn=13&vc=830841358023983D9003A7E3CDFBBD8D&uid=X8222iBKEbYDAF2iMnDigLnt&wlan=w'
        elif article['itemId'].startswith('C'):
            articleparam["articleid"] = 'https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid=' + article[
                'playid'] + '&client=androidapp&tsp=1607594618&vn=13&vc=830841358023983D9003A7E3CDFBBD8D&uid=X8222iBKEbYDAF2iMnDigLnt&wlan=w'
        else:
            articleparam["articleid"] = 'https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid=' + article[
                'playid'] + '&client=androidapp&tsp=1607594618&vn=13&vc=830841358023983D9003A7E3CDFBBD8D&uid=X8222iBKEbYDAF2iMnDigLnt&wlan=w'
    else:
        articleparam["articleid"] = 'https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid=' + article[
            'playid'] + '&client=androidapp&tsp=1607594618&vn=13&vc=830841358023983D9003A7E3CDFBBD8D&uid=X8222iBKEbYDAF2iMnDigLnt&wlan=w'
    # articleparam["channelid"] = article['channel']
    articleparam["channelname"] = channelname
    # articleparam["articleid"] = article['trackId']
    # articleparam["articletype"] = article['news_show_type']
    articleparam["articletitle"] = article['title']
    articleparam["banner"] = banner
    articleparam["imageurl"] = article['img1']
    # articleparam["articleurl"] = article['itemUrl']
    # articleparam["videos"] = article['title']
    # articleparam["videocover"] = article['title']
    # articleparam["pubtime"] = article['pubDate']
    # articleparam["createtime"] = article['title']
    # articleparam["updatetime"] = article['title']
    articleparam["source"] = article['source']
    # articleparam["author"] = article['author']
    # articleparam["likenum"] = article['digg']
    # articleparam["commentnum"] = article['pl']
    # articleparam["readnum"] = article['title']
    # articleparam["sharenum"] = article['title']
    return articleparam


class YangShiYingYin(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "https://api.app.cctv.com/api/navigation/android/androidguanwang/7.0.0/cctvhome"
        # 频道请求头
        headers = {
            "User-Agent": "CntvCBox/CNTV_APP_CLIENT_CBOX_MOBILE VersionString/Android_7.0.4 OS/6.0.1",
            "X-Tingyun-Id": "85B-vX9WltU;c=2;r=370814658;u=a4a199712a698140f841ba6672db49959cfac62651eded497e1badb687f68831::C3D438955C7AF5EF",
            "Host": "api.app.cctv.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        # # 频道数据体
        # data = {}
        # # 如果携带的是json数据体,用appjson发送
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
        for channel in channelslists['data']['templates']:
            channelid = channel['pageId']
            channelname = channel['appBarTitle']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)
        # channelid = channelslists['data']['templates'][10]['pageId']
        # channelname = channelslists['data']['templates'][10]['appBarTitle']
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
            url = 'https://api.app.cctv.com/api/page/android/HandheldApplicationSink/7.0.0/' + channelid
            # 频道请求头
            headers = {
                "User-Agent": "CntvCBox/CNTV_APP_CLIENT_CBOX_MOBILE VersionString/Android_7.0.4 OS/6.0.1",
                "X-Tingyun-Id": "85B-vX9WltU;c=2;r=370814658;u=a4a199712a698140f841ba6672db49959cfac62651eded497e1badb687f68831::C3D438955C7AF5EF",
                "Host": "api.app.cctv.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
            }
            # # 频道数据体
            # data = {}
            # # 如果携带的是json数据体,用appjson发送
            # channel_json = {}
            # 频道请求方式
            # 若数据体以json形式发送则以下面方式发送数据上面方式注释
            # 频道请求方式
            method = "get"
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
            banners = articleslist_res.get("banner")
            channelname = articleslist_res.get("channelname")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                # 可在下面打印处打断点，查看请求到的数据
                # print(articlelist_json)
                # 若banner图在articlelist_json中则分来开取并给其复制banner = 1
                try:
                    templates = articlelist_json['data']['templates']
                    for template in templates:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        # print(template)
                        # print('每个item数量：', len(template['items']))
                        banner = 0
                        if '轮播图' in template["title"]:
                            banner = 1
                        for item in template['items']:
                            if ('playid' in item.keys() and item['playid'] != '' and (
                                    not item['playid'].startswith('EPGC'))) \
                                    or ('itemId' in item.keys() and
                                        (not item['itemId'].startswith('EPGC')) and
                                        (item['itemId'].endswith('.json') or item['itemId'].startswith('VSET') or item[
                                            'itemId'].startswith('ART') or item[
                                             'itemId'].startswith('PHO'))) \
                                    or ('itemUrl' in item.keys() and item['itemUrl'] != ''):
                                articleparam = InitClass().article_list_fields()
                                articleparam = setArticleListParam(channelname, banner, articleparam, item)

                                articlesparams.append(articleparam)
                            else:
                                print(
                                    f'title={item["title"]},playid={item["playid"]},itemId={item["itemId"]},itemUrl={item["itemUrl"]}')
                    # print('总数量：', len(articlesparams))
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
        for articleparam in articles:
            print(
                f'articletitle={articleparam["articletitle"]},articleid={articleparam["articleid"]},articleurl={articleparam["articleurl"]}')

            if articleparam["articleurl"]:
                continue
            url = articleparam["articleid"]
            headers = {}
            data = {}
            method = 'get'

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
                                                             data=data,
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
            articleid = articleres.get("articleid")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["imageurl"] = imgurl
            fields["banner"] = banners
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                # print(articlejson)

                fields["appname"] = appname
                if articleid.startswith('https://api.app.cctv.com/api/album/'):
                    fields["url"] = articlejson['data']['album']['url']  # 文章的html网址，提取shareurl
                    fields["workerid"] = articlejson['data']['album']['contentId']  # 文章的id
                    fields["title"] = articlejson['data']['album']['title']  # 文章的标题
                    # fields["content"] = articlejson['data']['article']['content']  # 文章的内容详情
                    fields["articlecovers"] = articlejson['data']['album']['logo']  # 文章的封面，一般为上面get到的字段
                    fields["images"] = json.dumps(articlejson['data']['photos'])  # 文章详情内的图片url，一般为列表需遍历获取
                    # fields["videos"] = articlejson['video']['lowChapters'][0]['url']  # 文章的视频链接地址
                    # fields["videocover"] = articlejson['video']['lowChapters'][0]['image']  # 文章的视频封面地址
                    # fields["width"] = width #文章的视频宽
                    # fields["height"] = height #文章的视频高
                    fields["source"] = articlejson['data']['album']['source']  # 文章的来源
                    fields["pubtime"] = articlejson['data']['album']['publishDateTime']  # 文章的发布时间
                    # fields["createtime"] = articlejson['f_pgmtime']  # 文章的发布时间
                    # fields["updatetime"] = articlejson['f_pgmtime']  # 文章的更新时间
                    # fields["likenum"] = likenum #文章的点赞数
                    # fields["playnum"] = playnum #视频的播放数
                    # fields["commentnum"] = commentnum #文章评论数
                    # fields["readnum"] = readnum #文章的阅读数
                    # fields["trannum"] = trannum #文章的转发数
                    # fields["sharenum"] = sharenum #文章分享数
                    # fields["author"] = author #文章作者
                elif articleid.startswith('https://api.app.cctv.com/api/article/'):
                    # fields["url"] = articleurl #文章的html网址，提取shareurl
                    fields["workerid"] = articlejson['data']['article']['contentId']  # 文章的id
                    fields["title"] = articlejson['data']['article']['title']  # 文章的标题
                    fields["content"] = articlejson['data']['article']['content']  # 文章的内容详情
                    fields["articlecovers"] = articlejson['data']['article']['logo']  # 文章的封面，一般为上面get到的字段
                    fields["images"] = articlejson['data']['article']['logo']  # 文章详情内的图片url，一般为列表需遍历获取
                    # fields["videos"] = articlejson['video']['lowChapters'][0]['url']  # 文章的视频链接地址
                    # fields["videocover"] = articlejson['video']['lowChapters'][0]['image']  # 文章的视频封面地址
                    # fields["width"] = width #文章的视频宽
                    # fields["height"] = height #文章的视频高
                    fields["source"] = articlejson['data']['article']['source']  # 文章的来源
                    fields["pubtime"] = articlejson['data']['article']['publishDateTime']  # 文章的发布时间
                    # fields["createtime"] = articlejson['f_pgmtime']  # 文章的发布时间
                    # fields["updatetime"] = articlejson['f_pgmtime']  # 文章的更新时间
                    # fields["likenum"] = likenum #文章的点赞数
                    # fields["playnum"] = playnum #视频的播放数
                    # fields["commentnum"] = commentnum #文章评论数
                    # fields["readnum"] = readnum #文章的阅读数
                    # fields["trannum"] = trannum #文章的转发数
                    # fields["sharenum"] = sharenum #文章分享数
                    # fields["author"] = author #文章作者
                elif articleid.startswith("https://api.app.cctv.com/api/getVideoPageDetail?videoSetContentId="):
                    # fields["url"] = articleurl #文章的html网址，提取shareurl
                    fields["workerid"] = articlejson['data']['videoSetInfo']['vsetid']  # 文章的id
                    fields["title"] = articlejson['data']['videoSetInfo']['title']  # 文章的标题
                    fields["content"] = articlejson['data']['videoSetInfo']['brief']  # 文章的内容详情
                    # fields["articlecovers"] = articlejson['video']['lowChapters'][0]['image']  # 文章的封面，一般为上面get到的字段
                    fields["images"] = articlejson['data']['videoSetInfo']['image']  # 文章详情内的图片url，一般为列表需遍历获取
                    # fields["videos"] = articlejson['video']['lowChapters'][0]['url']  # 文章的视频链接地址
                    # fields["videocover"] = articlejson['video']['lowChapters'][0]['image']  # 文章的视频封面地址
                    # fields["width"] = width #文章的视频宽
                    # fields["height"] = height #文章的视频高
                    # fields["source"] = source  # 文章的来源
                    # fields["pubtime"] = articlejson['f_pgmtime']  # 文章的发布时间
                    # fields["createtime"] = articlejson['f_pgmtime']  # 文章的发布时间
                    # fields["updatetime"] = articlejson['f_pgmtime']  # 文章的更新时间
                    # fields["likenum"] = likenum #文章的点赞数
                    # fields["playnum"] = playnum #视频的播放数
                    # fields["commentnum"] = commentnum #文章评论数
                    # fields["readnum"] = readnum #文章的阅读数
                    # fields["trannum"] = trannum #文章的转发数
                    # fields["sharenum"] = sharenum #文章分享数
                    # fields["author"] = author #文章作者
                elif articleid.startswith("https://api.app.cctv.com/api/getVideoPageDetail?videoGuid="):
                    # fields["url"] = articleurl #文章的html网址，提取shareurl
                    fields["workerid"] = articlejson['data']['videoInfo']['guid']  # 文章的id
                    fields["title"] = articlejson['data']['videoInfo']['title']  # 文章的标题
                    if 'videoRoughCut' in articlejson['data'].keys():
                        fields["content"] = articlejson['data']['videoRoughCut']  # 文章的内容详情
                    # fields["articlecovers"] = articlejson['video']['lowChapters'][0]['image']  # 文章的封面，一般为上面get到的字段
                    # fields["images"] = articlejson['video']['lowChapters'][0]['image']  # 文章详情内的图片url，一般为列表需遍历获取
                    # fields["videos"] = articlejson['video']['lowChapters'][0]['url']  # 文章的视频链接地址
                    # fields["videocover"] = articlejson['video']['lowChapters'][0]['image']  # 文章的视频封面地址
                    # fields["width"] = width #文章的视频宽
                    # fields["height"] = height #文章的视频高
                    # fields["source"] = source  # 文章的来源
                    # fields["pubtime"] = articlejson['f_pgmtime']  # 文章的发布时间
                    # fields["createtime"] = articlejson['f_pgmtime']  # 文章的发布时间
                    # fields["updatetime"] = articlejson['f_pgmtime']  # 文章的更新时间
                    # fields["likenum"] = likenum #文章的点赞数
                    # fields["playnum"] = playnum #视频的播放数
                    # fields["commentnum"] = commentnum #文章评论数
                    # fields["readnum"] = readnum #文章的阅读数
                    # fields["trannum"] = trannum #文章的转发数
                    # fields["sharenum"] = sharenum #文章分享数
                    # fields["author"] = author #文章作者
                elif articleid.startswith('https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid='):
                    # fields["url"] = articleurl #文章的html网址，提取shareurl
                    fields["workerid"] = articlejson['client_sid']  # 文章的id
                    fields["title"] = articlejson['title']  # 文章的标题
                    # fields["content"] = content #文章的内容详情
                    fields["articlecovers"] = articlejson['video']['lowChapters'][0]['image']  # 文章的封面，一般为上面get到的字段
                    fields["images"] = articlejson['video']['lowChapters'][0]['image']  # 文章详情内的图片url，一般为列表需遍历获取
                    fields["videos"] = articlejson['video']['lowChapters'][0]['url']  # 文章的视频链接地址
                    fields["videocover"] = articlejson['video']['lowChapters'][0]['image']  # 文章的视频封面地址
                    # fields["width"] = width #文章的视频宽
                    # fields["height"] = height #文章的视频高
                    # fields["source"] = source  # 文章的来源
                    fields["pubtime"] = articlejson['f_pgmtime']  # 文章的发布时间
                    fields["createtime"] = articlejson['f_pgmtime']  # 文章的发布时间
                    fields["updatetime"] = articlejson['f_pgmtime']  # 文章的更新时间
                    # fields["likenum"] = likenum #文章的点赞数
                    # fields["playnum"] = playnum #视频的播放数
                    # fields["commentnum"] = commentnum #文章评论数
                    # fields["readnum"] = readnum #文章的阅读数
                    # fields["trannum"] = trannum #文章的转发数
                    # fields["sharenum"] = sharenum #文章分享数
                    # fields["author"] = author #文章作者
                else:
                    print(articlejson)
                    # fields["url"] = articlejson['data']['lowChapters'] #文章的html网址，提取shareurl
                    fields["workerid"] = articlejson['data']['PageId']  # 文章的id
                    fields["title"] = articlejson['data']['title']  # 文章的标题
                    fields["content"] = articlejson['data']['itemList']  # 文章的内容详情
                    # fields["articlecovers"] = articlejson['data']['lowChapters'] #文章的封面，一般为上面get到的字段
                    # fields["images"] = articlejson['data']['itemList'][0]['imgUrl'] #文章详情内的图片url，一般为列表需遍历获取
                    # fields["videos"] = articlejson['data']['lowChapters'] #文章的视频链接地址
                    # fields["videocover"] =  articlejson['data']['itemList'][0]['imgUrl'] #文章的视频封面地址
                    # fields["width"] = articlejson['data']['lowChapters'] #文章的视频宽
                    # fields["height"] = articlejson['data']['lowChapters'] #文章的视频高
                    # fields["source"] = articlejson['data']['lowChapters'] #文章的来源
                    # fields["pubtime"] = articlejson['data']['lowChapters'] #文章的发布时间
                    # fields["createtime"] = articlejson['data']['lowChapters'] #文章的发布时间
                    # fields["updatetime"] = articlejson['data']['lowChapters'] #文章的更新时间
                    # fields["likenum"] = articlejson['data']['lowChapters'] #文章的点赞数
                    # fields["playnum"] = articlejson['data']['lowChapters'] #视频的播放数
                    # fields["commentnum"] = articlejson['data']['lowChapters'] #文章评论数
                    # fields["readnum"] = articlejson['data']['lowChapters'] #文章的阅读数
                    # fields["trannum"] = articlejson['data']['lowChapters'] #文章的转发数
                    # fields["sharenum"] = articlejson['data']['lowChapters'] #文章分享数
                    # fields["author"] = articlejson['data']['lowChapters'] #文章作者
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
    spider = YangShiYingYin('央视影音')
    spider.run()
