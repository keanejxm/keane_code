# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import json

import requests

from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass


def setArticleListParam(channelname, banner, articleparam, article):
    articleparam["channelid"] = article['cmsColumnId']
    articleparam["channelname"] = channelname
    articleparam["articleid"] = article['cmsContentId']
    articleparam["articletype"] = article['type']
    articleparam["articletitle"] = article['title']
    # articleparam["channelname"] = article['title']
    articleparam["banner"] = banner
    articleparam["imageurl"] = article['img']
    # articleparam["articleurl"] = article['title']
    # articleparam["videos"] = article['title']
    # articleparam["videocover"] = article['title']
    articleparam["pubtime"] = article['publishDate']
    articleparam["createtime"] = article['createDate']
    # articleparam["updatetime"] = article['title']
    # articleparam["source"] = article['title']
    articleparam["author"] = article['author']
    # articleparam["likenum"] = article['digg']
    # articleparam["commentnum"] = article['pl']
    # articleparam["readnum"] = article['title']
    # articleparam["sharenum"] = article['title']
    return articleparam


class GuoXin(Appspider):

    @staticmethod
    def get_app_params():
        """
        组合请求频道的数据体
        :return:
        """
        # 频道url
        url = "http://app.phonemovie.cnlive.com/gxb/api/page"
        # 频道请求头
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "186",
            "Host": "app.phonemovie.cnlive.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.7.0",
        }
        # 频道数据体
        dataParams = {"appid": "gxb",
                      "pageType": "channelList",
                      "pageUUID": "852cde69-ecd8-11e6-b52e-c7d8a7a18cc4",
                      "plat": "a",
                      "version": "5.0"
                      }
        data = {'params': json.dumps(dataParams)}
        # 如果携带的是json数据体,用appjson发送
        # app_json = {}
        # 频道请求方式
        method = "post"
        app_params = InitClass().app_params(url, headers, method, data=data)
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
        for channel in channelslists['ininav']['programs']:
            channelid = channel['cid']
            channelname = channel['title']
            channelparam = InitClass().channel_fields(channelid, channelname)
            channelparams.append(channelparam)
        channelParamFbhhf = InitClass().channel_fields('spzl/fbhhf/', '发布会回放')
        channelparams.append(channelParamFbhhf)
        channelParamFbhgg = InitClass().channel_fields('spzl/fbhgg/', '发布会预告')
        channelparams.append(channelParamFbhgg)
        channelParamGxzs = InitClass().channel_fields('spzl/gxzs/', '国新之声')
        channelparams.append(channelParamGxzs)
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
            url = 'http://app.phonemovie.cnlive.com/gxb/api/cataloglatest'
            headers = {
                "Accept": "application/json",
                "X-Tingyun-Id": "V03APpUPw3U;c=2;r=925998793;",
                "Content-Type": "application/x-www-form-urlencoded",
                "Content-Length": "202",
                "Host": "app.phonemovie.cnlive.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.7.0",
            }
            # 频道数据体{"appid":"gxb","categoryId":"wz/dfdt/","lang":"cn","page":"1","pageSize":"10","plat":"a","version":"5.0"}
            dataParams = {"appid": "gxb",
                          "categoryId": channelid,
                          "lang": "cn",
                          "page": "1",
                          "pageSize": "10",
                          "plat": "a",
                          "version": "5.0"
                          }
            data = {'params': json.dumps(dataParams)}
            # 如果携带的是json数据体,用appjson发送
            # channeljson = { }
            method = 'post'
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
                if 'ttName' in articlelist_json.keys() and 'programs' in articlelist_json['ttName'].keys():
                    for article in articlelist_json['ttName']['programs']:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        articleparam = InitClass().article_list_fields()
                        articleparam = setArticleListParam(channelname, 1, articleparam, article)
                        articlesparams.append(articleparam)
                if 'programs' in articlelist_json.keys():
                    for article in articlelist_json['programs']:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        articleparam = InitClass().article_list_fields()
                        articleparam = setArticleListParam(channelname, 0, articleparam, article)
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
            "Accept": "application/json",
            "X-Tingyun-Id": "V03APpUPw3U;c=2;r=925998793;",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "202",
            "Host": "app.phonemovie.cnlive.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.7.0",
        }
        # 频道数据体{"appid":"gxb","categoryId":"wz/dfdt/","lang":"cn","page":"1","pageSize":"10","plat":"a","version":"5.0"}
        data = {}
        method = 'post'
        for articleparam in articles:
            articletype = articleparam.get("articletype")
            if 'album' == articletype:
                print(articleparam)
            elif 'article' == articletype:
                url = 'http://app.phonemovie.cnlive.com/gxb/api/programByContentId'
                dataParams = {"appid": "38_ivkou3xi05",
                              "cmsContentId": articleparam.get("articleid"),
                              "plat": "a",
                              "version": "5.0"
                              }
                data = {'params': json.dumps(dataParams)}

            elif 'audio' == articletype:
                print(articleparam)
            elif 'Banner' == articletype:
                print(articleparam)
            elif 'LK' == articletype:
                print(articleparam)
            elif 'live' == articletype:
                print(articleparam)
            elif 'subject' == articletype:
                url = 'http://app.phonemovie.cnlive.com/gxb/api/objectContent'
                dataParams = {"appid": "38_ivkou3xi05",
                              "cmsContentId": articleparam.get("articleid"),
                              "plat": "a",
                              "version": "5.0"
                              }
                data = {'params': json.dumps(dataParams)}
            elif 'program' == articletype:
                url = 'http://app.phonemovie.cnlive.com/gxb/api/programByContentId'
                dataParams = {"appid": "38_ivkou3xi05",
                              "cmsContentId": articleparam.get("articleid"),
                              "plat": "a",
                              "version": "5.0"
                              }
                data = {'params': json.dumps(dataParams)}
            elif 'videoArticle' == articletype:
                print(articleparam)
            else:
                print(articleparam)

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
            article_show = InitClass().article_params_fields(url, headers, method, channelname, imgurl,
                                                             data=data,
                                                             videourl=videos, videocover=videocover, pubtime=pubtime,
                                                             createtime=createtime, updatetime=updatetime,
                                                             source=source, author=author, likenum=likenum,
                                                             commentnum=channelid, sharenum=sharenum,
                                                             readnum=articletype,
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
            # 若上面存储了此字段需用下列方式获取
            channelid = articleres.get("commentnum")
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
                url = ''
                headers = {
                    "Accept": "application/json",
                    "X-Tingyun-Id": "V03APpUPw3U;c=2;r=925998793;",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": "202",
                    "Host": "app.phonemovie.cnlive.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.7.0",
                }
                # 频道数据体{"appid":"gxb","categoryId":"wz/dfdt/","lang":"cn","page":"1","pageSize":"10","plat":"a","version":"5.0"}
                if 'album' == articletype:
                    print(articlejson)
                elif 'article' == articletype:
                    url = 'http://app.phonemovie.cnlive.com/gxb/api/programDetail'
                    dataParams = {"appid": "gxb",
                                  "id": articleid,
                                  "plat": "a",
                                  "type": "article",
                                  "version": "5.0"}
                    data = {'params': json.dumps(dataParams)}
                    response = requests.post(url=url, headers=headers, data=data).content.decode()
                    articlejson1 = json.loads(json.dumps(json.loads(response), indent=4, ensure_ascii=False))
                    print(articlejson1)
                    fields["url"] = articlejson['program']['pageUrl']  # 文章的html网址，提取shareurl
                    fields["workerid"] = articleid  # 文章的id
                    fields["title"] = articlejson['program']['title']  # 文章的标题
                    fields["content"] = articlejson1['content']  # 文章的内容详情

                    fields["articlecovers"] = [articlejson['program']['img']]  # 文章的封面，一般为上面get到的字段
                    fields["images"] = InitClass().get_images(fields["content"])  # 文章详情内的图片url，一般为列表需遍历获取
                    # fields["videos"] = articlejson['data']['link']  # 文章的视频链接地址
                    # fields["videocover"] = articlejson['data']['link']  # 文章的视频封面地址
                    # fields["width"] = articlejson['data']['link']  # 文章的视频宽
                    # fields["height"] = articlejson['data']['link']  # 文章的视频高
                    # fields["source"] = articlejson['data']['category']  # 文章的来源
                    fields["pubtime"] = InitClass().date_time_stamp(articlejson['program']['publishDate'])  # 文章的发布时间
                    fields["createtime"] = InitClass().date_time_stamp(articlejson['program']['createDate'])  # 文章的发布时间
                    # fields["updatetime"] = articlejson['data']['pubDate']  # 文章的更新时间
                    # fields["likenum"] = articlejson['data']['goodpost']  # 文章的点赞数
                    # fields["playnum"] = articlejson['data']['link']  # 视频的播放数
                    # fields["commentnum"] = len(articlejson['data']['comments'])  # 文章评论数
                    # fields["readnum"] = articlejson['data']['click']  # 文章的阅读数
                    # fields["trannum"] = articlejson['data']['link']  # 文章的转发数
                    # fields["sharenum"] = articlejson['data']['link']  # 文章分享数
                    fields["author"] = articlejson['program']['author']  # 文章作者

                elif 'audio' == articletype:
                    print(articlejson)
                elif 'Banner' == articletype:
                    print(articlejson)
                elif 'LK' == articletype:
                    print(articlejson)
                elif 'live' == articletype:
                    print(articlejson)
                elif 'subject' == articletype:
                    print(articlejson)
                    # fields["url"] = articlejson['program']['pageUrl']  # 文章的html网址，提取shareurl
                    fields["workerid"] = articleid  # 文章的id
                    fields["title"] = articlejson['programs'][0]['title']  # 文章的标题
                    fields["content"] = json.dumps(articlejson['programs'][0]['list'])  # 文章的内容详情

                    fields["articlecovers"] = [articlejson['titleImage']]  # 文章的封面，一般为上面get到的字段
                    # fields["images"] = articlejson['titleImage']  # 文章详情内的图片url，一般为列表需遍历获取
                    # fields["videos"] = articlejson['program']['videoUrl']  # 文章的视频链接地址
                    # fields["videocover"] = articlejson['data']['link']  # 文章的视频封面地址
                    # fields["width"] = articlejson['data']['link']  # 文章的视频宽
                    # fields["height"] = articlejson['data']['link']  # 文章的视频高
                    # fields["source"] = articlejson['data']['category']  # 文章的来源
                    # fields["pubtime"] = articlejson['program']['publishDate']  # 文章的发布时间
                    # fields["createtime"] = articlejson['program']['createDate']  # 文章的发布时间
                    # fields["updatetime"] = articlejson['data']['pubDate']  # 文章的更新时间
                    # fields["likenum"] = articlejson['data']['goodpost']  # 文章的点赞数
                    # fields["playnum"] = articlejson['data']['link']  # 视频的播放数
                    # fields["commentnum"] = len(articlejson['data']['comments'])  # 文章评论数
                    # fields["readnum"] = articlejson['data']['click']  # 文章的阅读数
                    # fields["trannum"] = articlejson['data']['link']  # 文章的转发数
                    # fields["sharenum"] = articlejson['data']['link']  # 文章分享数
                    # fields["author"] = articlejson['program']['author']  # 文章作者
                elif 'program' == articletype:
                    url = 'http://app.phonemovie.cnlive.com/gxb/api/programDetail'
                    dataParams = {"appid": "gxb",
                                  "id": articleid,
                                  "plat": "a",
                                  "type": "article",
                                  "version": "5.0"}
                    data = {'params': json.dumps(dataParams)}
                    response = requests.post(url=url, headers=headers, data=data).content.decode()
                    articlejson1 = json.loads(json.dumps(json.loads(response), indent=4, ensure_ascii=False))
                    fields["url"] = articlejson['program']['pageUrl']  # 文章的html网址，提取shareurl
                    fields["workerid"] = articleid  # 文章的id
                    fields["title"] = articlejson['program']['title']  # 文章的标题
                    fields["content"] = articlejson1['content']  # 文章的内容详情

                    fields["articlecovers"] = [articlejson['program']['img']]  # 文章的封面，一般为上面get到的字段
                    # fields["images"] = articlejson['program']['img']  # 文章详情内的图片url，一般为列表需遍历获取
                    fields["videos"] = [articlejson['program']['videoUrl']]  # 文章的视频链接地址
                    # fields["videocover"] = articlejson['data']['link']  # 文章的视频封面地址
                    # fields["width"] = articlejson['data']['link']  # 文章的视频宽
                    # fields["height"] = articlejson['data']['link']  # 文章的视频高
                    # fields["source"] = articlejson['data']['category']  # 文章的来源
                    fields["pubtime"] = InitClass().date_time_stamp(articlejson['program']['publishDate'])  # 文章的发布时间
                    fields["createtime"] = InitClass().date_time_stamp(articlejson['program']['createDate'])  # 文章的发布时间
                    # fields["updatetime"] = articlejson['data']['pubDate']  # 文章的更新时间
                    # fields["likenum"] = articlejson['data']['goodpost']  # 文章的点赞数
                    # fields["playnum"] = articlejson['data']['link']  # 视频的播放数
                    # fields["commentnum"] = len(articlejson['data']['comments'])  # 文章评论数
                    # fields["readnum"] = articlejson['data']['click']  # 文章的阅读数
                    # fields["trannum"] = articlejson['data']['link']  # 文章的转发数
                    # fields["sharenum"] = articlejson['data']['link']  # 文章分享数
                    fields["author"] = articlejson['program']['author']  # 文章作者
                elif 'videoArticle' == articletype:
                    print(articlejson)
                else:
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
    spider = GuoXin('国新')
    spider.run()
