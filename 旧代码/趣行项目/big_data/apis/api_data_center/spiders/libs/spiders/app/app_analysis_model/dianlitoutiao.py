# Author ava
# coding=utf-8
# @Time    : 2020/12/7 10:38
# @File    : yangshixinwen.py
# @Software: PyCharm
import bs4
import requests
import json
import re

from spiders.libs.spiders.app.appspider_m import Appspider
from spiders.libs.spiders.app.initclass import InitClass


class DianLiTouTiao(Appspider):

    @staticmethod
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
        channelslists = json.loads(channelsres)
        for channel in channelslists['info']:
            channelid = channel
            channelname = channel
            channelparam = InitClass().channel_fields(channelid, channelname)
            yield channelparam

    def getarticlelistparams(self, channelsres):
        """
        此方法目的是组建请求文章列页面数据参数，url，headers，data，若以json形式发送数据，则channeljson = channeljson
        :param channelsparams:
        :return:
        """
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
            'Host': 'api.chinapower.org.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        method = 'get'
        channel_num = 1
        if channel_num == 1:
            newsUrl = "http://api.chinapower.org.cn/index.php/index/index/selfNews?page=1"
            videoUrl = 'http://api.chinapower.org.cn/index.php/index/index/findModule?page=1'
            channelname = "新闻"
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)
            articlelist_param = InitClass().articlelists_params_fields(newsUrl, headers, method, channelname,
                                                                       channel_index_id=channel_index_id)
            articlelist_param_video = InitClass().articlelists_params_fields(videoUrl, headers, method, channelname,
                                                                             channel_index_id=channel_index_id)
            yield channel_field, [articlelist_param, articlelist_param_video]
        for channel in self.analyzechannels(channelsres):
            channel_num += 1
            channelid = channel.get("channelid")
            channelname = channel.get("channelname")
            if channel_num == 2:
                data = {
                    'type': channelname,
                    'page': '1',
                    'pagesize': '20',
                    'pull': 'down',
                    'top': '1'
                }
            else:
                data = {
                    'type': channelname,
                    'page': '1',
                    'pagesize': '20',
                    'pull': 'down'
                }
            url = "http://api.chinapower.org.cn/index.php/index/news/category"
            self_typeid = self.self_typeid
            platform_id = self.platform_id
            platform_name = self.newsname
            channel_field, channel_index_id = InitClass().create_channel_index(platform_id, platform_name,
                                                                               self_typeid, channelname,
                                                                               channel_num)

            articlelist_param = InitClass().articlelists_params_fields(url, headers, method, channelname, data=data,
                                                                       channelid=channelname,
                                                                       channel_index_id=channel_index_id)
            yield channel_field, [articlelist_param]

    @staticmethod
    def analyze_articlelists(articleslist_ress):
        """
        解析文章列表页，目的是为了获取文章具体信息，组建请求文章详情数据体
        :param articleslist_ress:
        :return:
        """
        for articleslist_res in articleslist_ress:
            banners = articleslist_res.get("banner")
            channelname = articleslist_res.get("channelname")
            channel_index_id = articleslist_res.get("channelindexid")
            channelid = articleslist_res.get("channelid")
            articlelist_res = articleslist_res.get("channelres")
            articlelist_json = {}
            try:
                articlelist_json = json.loads(articlelist_res)
                # 若banner图在articlelist_json中则分来开取并给其复制banner = 1
                try:
                    articlelists = articlelist_json['info']
                    for article in articlelists:
                        # 可在下面打印处打断点，查看请求到的数据（用于解析json）
                        if 'self_type' in article:
                            articleparam = InitClass().article_list_fields()
                            articletitle = article['self_title']
                            articleid = article['self_id']
                            videos = [article["self_thumbnail_url"]]  # 在此处获取到文章视频url，避免在文章详情获取不到视频链接，数据类型list
                            videocover = [article["videocover"]]  # 在此处获取到文章视频封面图，避免在文章详情获取不到视频封面图链接，数据类型list
                            articleparam["videos"] = videos
                            articleparam["videocover"] = videocover
                        else:
                            articleparam = InitClass().article_list_fields()
                            articletitle = article['list_title']
                            articleid = article['list_id']
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
                        articleparam["channelindexid"] = channel_index_id
                        articleparam["channelid"] = channelname
                        articleparam["banner"] = banners
                        yield articleparam
                except Exception as e:
                    print(e, articlelist_json)
            except Exception as e:
                print(e, articlelist_json)

    def getarticleparams(self, articleslist_ress):
        """
        组建请求文章详情所需要的数据体
        :param articles:
        :return:
        """
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
        for articleparam in self.analyze_articlelists(articleslist_ress):
            data = {
                'list_id': articleparam.get("articleid"),
            }
            # 此处代码不需要改动
            channelname = articleparam.get("channelname")
            channel_index_id = articleparam.get("channelindexid")
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
            article = InitClass().article_params_fields(url, headers, method, channelname, imgurl, data=data,
                                                        videourl=videos, videocover=videocover, pubtime=pubtime,
                                                        createtime=createtime, updatetime=updatetime,
                                                        source=source, author=author, likenum=channelid,
                                                        commentnum=commentnum, sharenum=sharenum, readnum=readnum,
                                                        articleurl=articleurl, banners=banner,
                                                        channel_index_id=channel_index_id)
            yield [article]

    def analyzearticle(self,articles_res):
        for articleres in articles_res:
            channelname = articleres.get("channelname")
            channel_index_id = articleres.get("channelindexid")
            imgurl = articleres.get("images")
            appname = articleres.get("appname")
            banners = articleres.get("banner")
            articleres = articleres.get("articleres")
            fields = InitClass().article_fields()
            fields["channelname"] = channelname
            fields["images"] = imgurl
            fields["banner"] = banners
            fields["articlecovers"] = []  # 文章的封面，一般为上面get到的字段
            try:
                articlejson = json.loads(json.dumps(json.loads(articleres), indent=4, ensure_ascii=False))
                res = requests.get(articlejson['path'])
                res.encoding = res.apparent_encoding
                html = res.text
                bf = bs4.BeautifulSoup(html, 'html.parser')
                title = bf.find('h1').text
                source = bf.select('.avatar span')[0].text.replace('来源： ', '')
                pubtime = bf.select('.avatar span')[1].text.replace('时间：', '')
                content = bf.find('div', class_='text')
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
                fields["appname"] = self.newsname
                fields["platformID"] = self.platform_id
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
                fields["channelindexid"] = channel_index_id
                fields["pubtime"] = InitClass().date_time_stamp(InitClass().format_date(pubtime))
                fields = InitClass().wash_article_data(fields)
                yield {"code": 1, "msg": "OK", "data": {"works": fields}}
            except Exception as e:
                print(e)

def fetch_yield(appname, logger, platform_id, self_typeid):
    appspider = DianLiTouTiao(appname, logger, platform_id=platform_id, self_typeid=self_typeid)
    for article_data in appspider.fethch_yieldaaaa(appspider):
        yield article_data
