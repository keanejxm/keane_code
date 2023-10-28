# -*- encoding:utf-8 -*-
"""
@功能:第一财经解析模板
@AUTHOR：lucio
@文件名：diyicaijing.py
@时间：2020/12/31  17:33
"""

import json
from lxml import etree
from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass

headers = {
    'User-Agent': 'Mozilla/5.0  (Windows NT 10.0; WOW64) Appl'
                  'eWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
}


class DiYiCaiJing(Appspider):

    def analyze_channel(self):
        url = 'https://m.yicai.com/api/ajax/getnavs'
        channel_list = []
        r = self.send_request({
            'url': url,
            'headers': headers,
            'method': 'get',
        }).__next__()['request_res']
        datas = json.loads(r)
        for data in datas['header']['news']:
            channeid = data['ChannelID']
            url_channel = f'https://m.yicai.com/api/ajax/getlistbycid?cid={channeid}&page=1&pagesize=25'
            channel_list.append(url_channel)
        return channel_list

    def analyze_articlelists(self, url):
        r = self.send_request({
            'url': url,
            'headers': headers,
            'method': 'get',
        }).__next__()['request_res']
        datas = json.loads(r)
        for data in datas:
            article_item = InitClass().article_fields()

            article_item['appname'] = '第一财经'
            article_item['channelname'] = data['ChannelName']
            article_item['channelID'] = data['ChannelID']
            article_item['workerid'] = data['NewsID']
            # 判断是否为专题
            if data['thumbsType'] == 2 and '14' in str(data['NewsType']):
                article_item['url'] = f'https://m.yicai.com/api/ajax/getnewsdetail?id={data["EntityNews"]}'
                article_item['topicTitle'] = data['NewsTitle']

                self.get_topic(article_item)
            elif data['thumbsType'] == 2 and data['NewsType'] != 13:
                article_item['url'] = f'https://www.yicai.com/api/ajax/getnewsdetail?id={data["NewsID"]}'
                article_item['topicTitle'] = data['NewsTitle']

                self.get_topic(article_item)
            else:
                # pass
                article_item['title'] = data['NewsTitle']
                article_item['author'] = data['NewsAuthor']
                article_item['source'] = data['NewsSource']

                article_item['EntityNews'] = data['EntityNews']
                article_item['articlecovers'] = 'https:' + data['originPic']
                createdate = InitClass().date_time_stamp(data['CreateDate'].replace('T', ' '))
                article_item['url'] = f'https://m.yicai.com/news/{data["NewsID"]}.html'
                article_item['pubtime'] = createdate
                # print(article_item)
                if '11' == str(data['NewsType']):
                    article_item['url'] = f'https://m.yicai.com/api/ajax/getnewsdetail?id={data["NewsID"]}'
                    self.analyzearticle_11(article_item)
                elif '12' in str(data['NewsType']):
                    article_item['url'] = f'https://m.yicai.com/api/ajax/getnewsdetail?id={data["NewsID"]}'
                    self.analyzearticle_12(article_item)
                elif '10' in str(data['NewsType']):
                    # pass
                    self.analyzearticle(article_item)
            # break
        # print(datas)

    def get_topic(self, article_item):
        url = article_item['url']
        print(url)
        r = self.send_request({
            'url': url,
            'headers': headers,
            'method': 'get',
        }).__next__()['request_res']
        info_topic = json.loads(r)
        if info_topic['message'] == 'error':
            url = f'https://www.yicai.com/api/ajax/getnewsdetail?id={article_item["workerid"]}'
            r = self.send_request({
                'url': url,
                'headers': headers,
                'method': 'get',
            }).__next__()['request_res']
            info_topic = json.loads(r)
            print('更换url')
            print(url)
        for info in info_topic['result']['columnlist']:
            couumid = info['ColumnID']
            url_topic = f'https://m.yicai.com/api/ajax/getlistbycolumnid?cid={couumid}'
            r_ = self.send_request({
                'url': url_topic,
                'headers': headers,
                'method': 'get',
            }).__next__()['request_res']
            datas = json.loads(r_)
            for data in datas:
                article_item['title'] = data['NewsTitle']
                article_item['author'] = data['NewsAuthor']
                article_item['source'] = data['NewsSource']
                article_item['EntityNews'] = data['EntityNews']
                article_item['topicid'] = couumid
                article_item['articlecovers'] = 'https:' + data['originPic']
                createdate = InitClass().date_time_stamp(data['CreateDate'].replace('T', ' '))
                article_item['url'] = f'https://m.yicai.com/news/{data["NewsID"]}.html'
                article_item['pubtime'] = createdate
                # 处理图集特殊新闻
                if '11' == str(data['NewsType']):
                    article_item['url'] = f'https://m.yicai.com/api/ajax/getnewsdetail?id={data["NewsID"]}'
                    self.analyzearticle_11(article_item)
                elif '12' in str(data['NewsType']):
                    article_item['url'] = f'https://m.yicai.com/api/ajax/getnewsdetail?id={data["NewsID"]}'
                    self.analyzearticle_12(article_item)
                elif '10' in str(data['NewsType']):
                    # pass
                    self.analyzearticle(article_item)

    def analyzearticle(self, article_item):
        url = article_item['url']
        print(url)
        r = self.send_request({
            'url': url,
            'headers': headers,
            'method': 'get',
        }).__next__()['request_res']
        if r == 'error404':
            url = f'https://m.yicai.com/news/{article_item["EntityNews"]}.html'
            print('更换url')
            print(url)
            article_item['workerid'] = article_item.pop('EntityNews')
            r = self.send_request({
                'url': url,
                'headers': headers,
                'method': 'get',
            }).__next__()['request_res']

        html = etree.HTML(r)
        article_item['content'] = html.xpath('string(//*[@id="multi-text"])')
        article_item['images'] = html.xpath('//*[@id="multi-text"]//img/@src')
        if type(article_item['articlecovers']) != list:
            article_item['articlecovers'] = [article_item['articlecovers']]
        if type(article_item['images']) != list:
            article_item['images'] = [article_item['images']]
        if type(article_item['videos']) != list:
            article_item['videos'] = [article_item['videos']]
        if type(article_item['videocover']) != list:
            article_item['videocover'] = [article_item['videocover']]
        print(f'正在爬取{article_item.get("channelname")}频道')
        print(json.dumps(article_item, indent=4, ensure_ascii=False))

    # 图集新闻
    def analyzearticle_11(self, article_item):
        r = self.send_request({
            'url': article_item['url'],
            'headers': headers,
            'method': 'get',
        }).__next__()['request_res']
        datas = json.loads(r)
        article_item['content'] = datas['result']['sliders'][0]['note']
        article_list = []
        for data in datas['result']['sliders']:
            pic = 'https:' + data['pic']
            article_list.append(pic)
        article_item['images'] = article_list
        if type(article_item['articlecovers']) != list:
            article_item['articlecovers'] = [article_item['articlecovers']]
        if type(article_item['images']) != list:
            article_item['images'] = [article_item['images']]
        if type(article_item['videos']) != list:
            article_item['videos'] = [article_item['videos']]
        if type(article_item['videocover']) != list:
            article_item['videocover'] = [article_item['videocover']]
        print(f'正在爬取{article_item.get("channelname")}频道')
        print(json.dumps(article_item, indent=4, ensure_ascii=False))

    # 视频新闻
    def analyzearticle_12(self, article_item):
        r = self.send_request({
            'url': article_item['url'],
            'headers': headers,
            'method': 'get',
        }).__next__()['request_res']
        print(article_item['url'])
        data = json.loads(r)
        if r == 'error404' or data['message'] == 'error':
            url = f'https://m.yicai.com/api/ajax/getnewsdetail?id={article_item["EntityNews"]}.html'
            print('更换url')
            print(url)
            article_item['workerid'] = article_item.pop('EntityNews')
            r = self.send_request({
                'url': url,
                'headers': headers,
                'method': 'get',
            }).__next__()['request_res']
            data = json.loads(r)
        article_item['videos'] = data['result']['video']['videosrc']
        article_item['videocover'] = data['result']['video']['videopic']
        if type(article_item['articlecovers']) != list:
            article_item['articlecovers'] = [article_item['articlecovers']]
        if type(article_item['images']) != list:
            article_item['images'] = [article_item['images']]
        if type(article_item['videos']) != list:
            article_item['videos'] = [article_item['videos']]
        if type(article_item['videocover']) != list:
            article_item['videocover'] = [article_item['videocover']]
        print(f'正在爬取{article_item.get("channelname")}频道')
        print(json.dumps(article_item, indent=4, ensure_ascii=False))

    def run(self):
        channel_urls = self.analyze_channel()
        for url in channel_urls:
            self.analyze_articlelists(url)


if __name__ == '__main__':
    dycj = DiYiCaiJing('第一财经')
    dycj.run()
