# -*- encoding:utf-8 -*-
"""
@功能:武隆印象解析模板
@AUTHOR：lucio
@文件名：wulongyinxiang.py
@时间：2020/12/31  17:33
"""

import json
import re
from lxml import etree
from lib.templates.initclass import InitClass
from lib.templates.appspider_m import Appspider

headers = {
    'User-Agent': 'Mozilla/5.0  (Windows NT 10.0; WOW64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
}


class WuLongYinXiang(Appspider):

    def analyze_articlelists(self):
        channelsid = [['17005', '中央时政'], ['17006', '重庆时政'],
                      ['17007', '重庆时政'], ['724', '专题'], ['6456', '视听'],
                      ['722', '旅游']]
        for channel in channelsid:
            r = self.send_request( {
                'url': 'https://api.cqliving.com/info/news.html',
                'headers': headers,
                'method': 'post',
                'data': {'isCarousel': 'true',
                         'appId': '7',
                         'columnId': channel[0], }
            }).__next__()['request_res']

            data_channel = json.loads(r)
            # print(data_channel)
            for data in data_channel['data']['news']:
                article_item = InitClass().article_fields()
                article_item['channelID'] = data['columnsId']
                article_item['appname'] = '武隆印象移动端'
                article_item['channelname'] = channel[1]
                # 专题
                # print(data)
                if data['type'] == 2:
                    article_item['topicid'] = data['id']
                    article_item['topicTitle'] = data['title']
                    url_topic = 'https://api.cqliving.com/info/getSpecialDetail.html'
                    r_ = self.send_request( {
                        'url': url_topic,
                        'headers': headers,
                        'method': 'post',
                        'data': {
                            'appId': '7',
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

                    article_item['title'] = data['title']
                    article_item['workerid' \
                                 ''] = data['id']
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
                print(json.dumps(article_item, indent=4, ensure_ascii=False))
            # break

    def analyzearticle(self, article_item):
        # print(json.dumps(article_item, indent=4, ensure_ascii=False))
        url = article_item['url']
        print(url)
        if 'xhpfmapi' in url:
            id_ = re.findall(r"share/(\d+)", url)[0]
            url_ = f'https://xhpfmapi.zhongguowangshi.com/v600/news/{id_}.js?ts=0&share=1'
            print(url_)
            r = self.send_request( {
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
            article_item['content'] = data['content']
            print(f'正在爬取{article_item["channelname"]}频道')
            print(json.dumps(article_item, indent=4, ensure_ascii=False))
        elif 'isOpenApp=isOpenApp' in url:
            r = self.send_request( {
                'url': url,
                'headers': headers,
                'method': 'get',
            }).__next__()['request_res']
            html = etree.HTML(r)
            article_item['content'] = html.xpath('string(//*[@id="detail"]/div[@class="detail_content"])')
            # if not article_item['content']:
            #     article_item['content'] = html.xpath('string(//*[@id="detail"]/div[4])')
            article_item['images'] = html.xpath('//*[@id="detail"]/div[4]//img/@data-original')
            article_item['videos'] = html.xpath('//*[@id="detail"]/div[4]//video/source/@src')
            article_item['videocover'] = html.xpath('//*[@id="detail"]/div[4]//video/@poster')
            print(f'正在爬取{article_item["channelname"]}频道')
            print(json.dumps(article_item, indent=4, ensure_ascii=False))
        elif 'detail?classId' in url:
            class_id = re.findall(r'classId=(\d+)', url)[0]
            news_id = re.findall(r'&id=(\d+)', url)[0]
            url_ = f'https://api.cqrb.cn/api/news/getDetails?classId={class_id}&newsId={news_id}'
            print(url_)
            r = self.send_request( {
                'url': url_,
                'headers': headers,
                'method': 'get',
            }).__next__()['request_res']
            data = json.loads(r)
            article_item['images'] = data['data']['allImage']
            article_item['content'] = data['data']['contents']
            article_item['videos'] = data['data']['videoUrl']
            print(f'正在爬取{article_item["channelname"]}频道')
            print(json.dumps(article_item, indent=4, ensure_ascii=False))
            # print(data)
        else:
            try:
                r = self.send_request( {
                    'url': url,
                    'headers': headers,
                    'method': 'get',
                }).__next__()['request_res']
                html = etree.HTML(r)
            except UnicodeDecodeError as e:
                r = self.send_request( {
                    'url': url,
                    'headers': headers,
                    'method': 'get',
                }, code='gb2312').__next__()['request_res']
                html = etree.HTML(r)
            article_item['content'] = html.xpath('string(//*[@id="p-detail"])')
            # 该APP引用其他网站新闻较多 格式不一
            if not article_item['content']:
                article_item['content'] = html.xpath('string(/html/body/div[7]/div[3]/div[1])')
            if not article_item['content']:
                article_item['content'] = html.xpath('string(//*[@id="js_content"]/section[2])')
            if not article_item['content']:
                article_item['content'] = html.xpath('string(//*[@id="text_area"])')

            article_item['images'] = html.xpath('//*[@id="detail"]/div[4]//img/@data-original')
            if not article_item['images']:
                article_item['images'] = html.xpath(
                    '//*[@id="root"]/div/div/div/div/div[2]/div[3]/div/p[3]/img/@src')
            if not article_item['images']:
                article_item['images'] = html.xpath(
                    '//*[@id="p-detail"]//img/@src')

            article_item['videos'] = html.xpath('//*[@id="detail"]/div[4]//video/source/@src')
            article_item['videocover'] = html.xpath('//*[@id="detail"]/div[4]//video/@poster')

        if not article_item['images']:
            imagess = re.findall(r"http(\S*).jpg", article_item['content'])
            images = list()
            for image in imagess:
                image_url = "http" + image + ".jpg"
                images.append(image_url)
            article_item['images'] = images
        if type(article_item['articlecovers']) != list:
            article_item['articlecovers'] = [article_item['articlecovers']]
        if type(article_item['images']) != list:
            article_item['images'] = [article_item['images']]
        if type(article_item['videos']) != list:
            article_item['videos'] = [article_item['videos']]
        if type(article_item['videocover']) != list:
            article_item['videocover'] = [article_item['videocover']]
        print(f'正在爬取{article_item["channelname"]}频道')
        print(json.dumps(article_item, indent=4, ensure_ascii=False))

    def run(self):
        self.analyze_articlelists()


if __name__ == '__main__':
    wlyx = WuLongYinXiang('武隆印象')
    wlyx.run()
