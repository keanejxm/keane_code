# -*- encoding:utf-8 -*-
"""
@功能:爱璧山解析模板
@AUTHOR：lucio
@文件名：aibishan.py
@时间：2020/12/31  17:33
"""

import requests
import json
import re
from lxml import etree

# from lib.templates.initclass import InitClass
# from lib.templates.appspider_m import Appspider
from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass

headers = {
    'User-Agent': 'Mozilla/5.0  (Windows NT 10.0; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
}


class AiBiShan(Appspider):

    def analyze_articlelists(self):
        channelsid = [['7343', '推荐'], ['7344', '璧山'], ['7348', '晒文旅'], ['204', '专题'], ['202', '视频'], ]
        for channel in channelsid:

            r = self.send_request({
                'url': 'https://api.cqliving.com/info/news.html',
                'headers': headers,
                'method': 'post',
                'data': {'isCarousel': 'true',
                         'appId': '11',
                         'columnId': channel[0], }
            }).__next__()['request_res']
            data_channel = json.loads(r)
            for data in data_channel['data']['news']:
                article_item = InitClass().article_fields()
                article_item['channelID'] = data['columnsId']
                article_item['appname'] = '爱璧山'
                article_item['channelname'] = channel[1]
                # 专题
                if data['type'] == 2:
                    article_item['topicid'] = data['id']
                    article_item['topicTitle'] = data['title']
                    url_topic = 'https://api.cqliving.com/info/getSpecialDetail.html'
                    r_ = self.send_request({
                        'url': url_topic,
                        'headers': headers,
                        'method': 'post',
                        'data': {
                            'appId': '11',
                            'infoClassifyId': data['id']}
                    }).__next__()['request_res']
                    data_topic = json.loads(r_)
                    for data_ in data_topic['data']['firstPageData']['dataList']:
                        article_item['title'] = data_['title']
                        article_item['workerid'] = data_['id']
                        article_item['readnum'] = data_['viewCount']
                        article_item['source'] = data_['infoSource']
                        article_item['width'] = data_['width']
                        article_item['hight'] = data_['hight']
                        article_item['likenum'] = data_['praiseCount']
                        article_item['articlecovers'] = data_['images']
                        article_item['url'] = data_['url']
                        article_item['pubtime'] = InitClass().date_time_stamp(data_['onlineTime'])
                        # print(data_)
                        self.analyzearticle(article_item)
                    # break
                elif data['type'] == 0:
                    # 视频
                    if channel[0] == '6002':
                        article_item['title'] = data['title']
                        article_item['workerid'] = data['id']
                        article_item['readnum'] = data['viewCount']
                        article_item['source'] = data['infoSource']
                        article_item['width'] = data['width']
                        article_item['hight'] = data['hight']
                        article_item['likenum'] = data['praiseCount']
                        article_item['articlecovers'] = data['images']
                        article_item['url'] = data['url']
                        article_item['videos'] = data['contentUrl']
                        article_item['videocover'] = data['shareImgUrl']
                        article_item['pubtime'] = InitClass().date_time_stamp(data['onlineTime'])
                        if type(article_item['articlecovers']) != list:
                            article_item['articlecovers'] = [article_item['articlecovers']]
                        if type(article_item['images']) != list:
                            article_item['images'] = [article_item['images']]
                        if type(article_item['videos']) != list:
                            article_item['videos'] = [article_item['videos']]
                        if type(article_item['videocover']) != list:
                            article_item['videocover'] = [article_item['videocover']]
                        print(json.dumps(article_item, indent=4, ensure_ascii=False))
                        # self.get_article(article_item)
                    else:
                        article_item['title'] = data['title']
                        article_item['workerid'] = data['id']
                        article_item['readnum'] = data['viewCount']
                        article_item['source'] = data['infoSource']
                        article_item['width'] = data['width']
                        article_item['hight'] = data['hight']
                        article_item['likenum'] = data['praiseCount']
                        article_item['articlecovers'] = data['images']
                        article_item['url'] = data['url']
                        article_item['pubtime'] = InitClass().date_time_stamp(data['onlineTime'])
                        # print(data)
                        self.analyzearticle(article_item)

            # break

    def analyzearticle(self, article_item):
        # print(json.dumps(article_item, indent=4, ensure_ascii=False))
        url = article_item['url']
        # print(url)
        if 'xhpfmapi' in url:
            id_ = re.findall(r"share/(\d+)", url)[0]
            url_ = f'https://xhpfmapi.zhongguowangshi.com/v600/news/{id_}.js?ts=0&share=1'
            # print(url_)
            r = self.send_request({
                'url': url_,
                'headers': headers,
                'method': 'get',
            }).__next__()['request_res']
            data = json.loads(r[18:])
            # article_item['images'] = data['imglist']w
            article_item['pubtime'] = InitClass().date_time_stamp(data['releasedate'])
            article_item['images'] = data['imglist']
            article_item['videos'] = data['videourl']
            article_item['videocover'] = data['videoimageurl']
            article_item['source'] = data['docSource']
            article_item['commentnum'] = data['comment']
        elif 'isOpenApp=isOpenApp' in url:
            r = self.send_request({
                'url': url,
                'headers': headers,
                'method': 'get',
            }).__next__()['request_res']
            html = etree.HTML(r)
            article_item['content'] = html.xpath('string(//*[@id="detail"]/div[@class="detail_content"])')
            article_item['images'] = html.xpath('//*[@id="detail"]/div[4]//img/@data-original')
        elif 'news.cctv' in url:
            # print(url)
            r = self.send_request({
                'url': url,
                'headers': headers,
                'method': 'get',
            }).__next__()['request_res']
            # print(r)
            html = etree.HTML(r)
            article_item['content'] = html.xpath('string(//*[@class="content_18313"])')
            article_item['images'] = html.xpath('//*[@class="content_18313"]//img/@src')
        elif 'app.cctv' in url:
            year = '20' + re.findall('(\d+)&fromapp', url)[0][:2]
            month = re.findall('(\d+)&fromapp', url)[0][2:4]
            day = re.findall('(\d+)&fromapp', url)[0][4:]
            id_ = re.findall('id=Arti(.*?)&fromapp', url)[0]
            url = f'http://m.news.cctv.com/{year}/{month}/{day}/ARTI{id_}.shtml'
            r = self.send_request({
                'url': url,
                'headers': headers,
                'method': 'get',
            }).__next__()['request_res']
            # print(r)
            html = etree.HTML(r)
            # print(r)
            article_item['content'] = html.xpath('string(//*[@class="cnt_bd"])')
            article_item['images'] = html.xpath('//*[@class="cnt_bd"]//img/@src')
            # print(article_item)

        else:
            try:
                r = self.send_request({
                    'url': url,
                    'headers': headers,
                    'method': 'get',
                }).__next__()['request_res']
                # print(r)
                html = etree.HTML(r)
                article_item['content'] = html.xpath('string(//*[@id="img-content"])')
                article_item['images'] = html.xpath('//*[@id="content"]//img/@src')
            except UnicodeDecodeError as E:
                r = self.send_request({
                    'url': url,
                    'headers': headers,
                    'method': 'get',
                }, code='gbk').__next__()['request_res']
                # print(r)
                html = etree.HTML(r)
                article_item['content'] = html.xpath('string(//*[@id="img-content"])')
                article_item['images'] = html.xpath('//*[@id="content"]//img/@src')
            # print(article_item)
            ''

        if not article_item['images']:
            imagess = re.findall(r"http(\S*).jpg", article_item['content'])
            images = list()
            for image in imagess:
                image_url = "http" + image + ".jpg"
                images.append(image_url)
            article_item['images'] = images
        # 更改数据类型
        if type(article_item['articlecovers']) != list:
            article_item['articlecovers'] = [article_item['articlecovers']]
        if type(article_item['images']) != list:
            article_item['images'] = [article_item['images']]
        if type(article_item['videos']) != list:
            article_item['videos'] = [article_item['videos']]
        if type(article_item['videocover']) != list:
            article_item['videocover'] = [article_item['videocover']]
        print(json.dumps(article_item, indent=4, ensure_ascii=False))
        print(f'正在爬取{article_item["channelname"]}频道')


    def run(self):
        self.analyze_articlelists()


if __name__ == '__main__':
    ob = AiBiShan('爱璧山')
    ob.run()
