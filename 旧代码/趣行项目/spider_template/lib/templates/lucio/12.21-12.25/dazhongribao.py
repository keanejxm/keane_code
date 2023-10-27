# -*- encoding:utf-8 -*-
"""
@功能:大众日报解析模板
@AUTHOR：lucio
@文件名：dazhongribao.py
@时间：2020/12/31  17:33
"""

import json
from lib.templates.initclass import InitClass
from lxml import etree
import re
from lib.templates.appspider_m import Appspider

headers = {
    'User-Agent': 'Mozilla/5.0  (Windows NT 10.0; WOW64) AppleWebKit'
                  '/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
}


class DaZhongRiBao(Appspider):

    def analyze_channel(self):
        channel_list = list()
        channel_list.append(
            'http://phoneapi2.xrdz.dzng.com/index.php/article/'
            'articleList?columnId=&page=1&vs=3&lastFileId=0&art_type=3&userId=0')
        url = 'http://dzrb.dzng.com/col/17.htmlx'
        r = self.send_request({
            'url': url,
            'headers': headers,
            'method': 'get',
        }).__next__()['request_res']
        html = etree.HTML(r)
        channelids = html.xpath('//*[@id="columns"]//a/@data-id') + [re.findall(r'col/(.*?)\.', i)[0] for i in
                                                                     html.xpath('//*[@id="top"]/div[2]/div[2]/a/@href')]
        for i in channelids:
            channel_url = f'http://phoneapi2.xrdz.dzng.com/index.php' \
                f'/article/articleList?columnId={i}&page=1&vs=3&lastFileId=0&userId=0'
            # print(channel_url)
            channel_list.append(channel_url)
        return channel_list

    def analyze_articlelists(self, url):
        r = self.send_request({
            'url': url,
            'headers': headers,
            'method': 'get',
        }).__next__()['request_res']
        datas = json.loads(r)
        for data in datas['list']:
            article_item = InitClass().article_fields()
            # 判断是否为列表 是列表再次遍历
            if data.get('articleList'):
                for data_ in data['articleList']:
                    article_item['appname'] = '大众日报'
                    article_item['channelname'] = data_.get('colName')
                    # print('data:', data_)
                    article_item['channelID'] = data_.get('colID')
                    article_item['articlecovers'] = data_.get('picSmall')
                    article_item['source'] = data_.get('source')
                    article_item['workerid'] = data_.get('fileId')
                    article_item['pubtime'] = InitClass().date_time_stamp(data_['publishtime'].replace('T', ' '))
                    article_item['url'] = f'http://phoneapi2.xrdz.dzng.com/index.php/app_' \
                        f'if/getArticleContent?articleId={data_["fileId"]}&colID={data_["colID"]}'
                    self.analyzearticle(article_item)
            else:
                article_item['appname'] = '大众日报'
                article_item['channelname'] = data.get('colName')
                # print('data:', data)
                article_item['channelID'] = data.get('colID')
                article_item['articlecovers'] = data.get('picSmall')
                article_item['source'] = data.get('source')
                article_item['workerid'] = data.get('fileId')
                article_item['pubtime'] = InitClass().date_time_stamp(data['publishtime'].replace('T', ' '))
                article_item['url'] = f'http://phoneapi2.xrdz.dzng.com/index.php/app_' \
                    f'if/getArticleContent?articleId={data["fileId"]}&colID={data["colID"]}'
                # print(article_item)
                self.analyzearticle(article_item)
            # break

    def analyzearticle(self, article_item):
        r = self.send_request({
            'url': article_item['url'],
            'headers': headers,
            'method': 'get',
        }).__next__()['request_res']
        data = json.loads(r)
        # print(data['position'])
        # print(data)
        if data['position'] == '3':
            print('内容为专题')
            # print(3)
            article_item['topicTitle'] = data['title']
            html = etree.HTML(data['content'])
            urls = html.xpath('//a/@href')
            print(urls)

            for href in urls:
                if 'content' in href:
                    print(href)
                    # article_item['title']
                    r_ = self.send_request({
                        'url': href,
                        'headers': headers,
                        'method': 'get',
                    }).__next__()['request_res']
                    r_.encoding = 'gbk'
                    info = etree.HTML(r_)
                    article_item['title'] = info.xpath('string(//*[@id="Text_title"]/@value)')
                    article_item['author'] = info.xpath('string(//*[@id="Text_author"]/@value)')
                    article_item['content'] = info.xpath('string(//*[@id="news-con"])')
                    article_item['topicid'] = 1
                    images = info.xpath('//*[@class="newspic"]/@src')
                    article_item['images'] = ['http://paper.dzwww.com/dzrb/' + re.findall(r'\.\./\.\./(.*)', i)[0] for i
                                              in images]
                    articlecovers = info.xpath('string(//*[@id="news-header"]/div[1]/div[2]/a[2]/@href)')
                    # print(articlecovers)
                    article_item['articlecovers'] = 'http://paper.dzwww.com/dzrb/' + \
                                                    re.findall(r'\.\./\.\./(.*)', articlecovers)[0]

                    # print(images)
                    article_item['pubtime'] = InitClass().date_time_stamp(
                        info.xpath('string(//*[@id="Text_date"]/@value)').replace(' ', ' '))
                    if type(article_item['articlecovers']) != list:
                        article_item['articlecovers'] = [article_item['articlecovers']]
                    if type(article_item['images']) != list:
                        article_item['images'] = [article_item['images']]
                    if type(article_item['videos']) != list:
                        article_item['videos'] = [article_item['videos']]
                    if type(article_item['videocover']) != list:
                        article_item['videocover'] = [article_item['videocover']]
                    print(json.dumps(article_item, indent=4, ensure_ascii=False))
                    # break
        else:

            article_item['content'] = data['content']
            article_item['title'] = data['title']
            article_item['author'] = data['author']
            try:
                article_item['images'] = [i['imageUrl'] for i in data['images'][0]['imagearray']]
            except:
                print('暂无音频图片')
            try:
                article_item['videos'] = [i['videoUrl'] for i in data['videos'][0]['videoarray']]
            except:
                print('暂无音频图片')
            try:
                article_item['videocover'] = [i['imageUrl'] for i in data['videos'][0]['videoarray']]
            except:
                print('暂无音频图片')

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
        print(channel_urls)
        for url in channel_urls:
            self.analyze_articlelists(url=url)


if __name__ == '__main__':
    dzrb = DaZhongRiBao('大众日报')
    dzrb.run()
