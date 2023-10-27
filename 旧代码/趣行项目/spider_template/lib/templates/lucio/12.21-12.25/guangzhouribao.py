# -*- encoding:utf-8 -*-
"""
@功能:广州日报解析模板
@AUTHOR：lucio
@文件名：guangzhouribao.py
@时间：2020/12/31  17:33
"""

import json
from lib.templates.initclass import InitClass
from lib.templates.appspider_m import Appspider
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0  (Windows NT 10.0; WOW64) AppleWeb'
                  'Kit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
}


class GuangZhouRiBao(Appspider):

    def analyze_channel(self):
        channel_list = []
        url = 'https://app.gzdaily.cn:4443/app_if//getColumns?siteId=4&parentColumnId=54&' \
              'version=0&columnType=-1&jsoncallback=angular.callbacks._1'
        r = self.send_request({
            'url': url,
            'headers': headers,
            'method': 'get',
        }).__next__()['request_res']
        # print(r)
        datas = json.loads(r[21:-1])
        # print(datas)
        for data in datas['columns']:
            # print(data)
            if data['columnID'] != 76:
                channelid = data['columnID']
                channelname = data['columnName']
                channel_url = f'https://app.gzdaily.cn:4443/app_if//getArticles?columnId={channelid}&l' \
                    f'astFileId=0&page=1&version=0&jsoncallback=angular.callbacks._j'
                d = [channelname, channel_url, channelid]
                channel_list.append(d)
            # break
        return channel_list
        # break

    def analyze_articlelists(self, l):
        url = l[1]
        print(url)
        r = self.send_request({
            'url': url,
            'headers': headers,
            'method': 'get',
        }).__next__()['request_res']
        datas = json.loads(r[21:-1])
        for data in datas['list']:
            # print(data)
            article_item = InitClass().article_fields()
            article_item['appname'] = '广州日报'
            article_item['channelname'] = l[0]
            article_item['channelID'] = l[2]

            # 判断是否为专题
            if data['articleType'] == 3:
                article_item['topicTitle'] = data.get('title')
                # 专题下的各个板块
                url_ = f'https://app.gzdaily.cn:4443/app_if//getColumns?siteId=4&parentColumnId={data["linkID"]}&' \
                    f'version=0&columnType=-1&jsoncallback=angular.callbacks._5:formatted'
                r_ = self.send_request({
                    'url': url_,
                    'headers': headers,
                    'method': 'get',
                }).__next__()['request_res']
                datas_ = json.loads(r_[31:-1])
                for data_ in datas_['columns']:
                    # print(data_)

                    url_topic = f'https://app.gzdaily.cn:4443/app_if//getArticles?columnId={data_["columnId"]}&' \
                        f'lastFileId=0&count=30&rowNumber=0&version=0&adv=1&jsoncallback=angular.callbacks._6'
                    r_topic = self.send_request({
                        'url': url_topic,
                        'headers': headers,
                        'method': 'get',
                    }).__next__()['request_res']
                    info = json.loads(r_topic[21:-1])
                    for info_ in info['list']:
                        # print(info_)
                        if info_['articleType'] == 6:
                            pass
                        else:
                            article_item['title'] = info_['title']
                            article_item['topicid'] = 1
                            article_item['author'] = info_['arthorName']
                            article_item['source'] = info_['source']
                            article_item['images'] = info_.get('pic_list')
                            article_item['videoUrl'] = info_.get('videoUrl')
                            article_item['workerid'] = info_['fileId']
                            article_item['pubtime'] = info_['version']
                            article_item['likenum'] = info_['countPraise']
                            article_item['sharenum'] = info_['countShare']
                            article_item['commentnum'] = info_['countDiscuss']
                            article_item['articlecovers'] = info_.get('pic_list_title')
                            article_item['readnum'] = info_.get('countClick')
                            article_item['topicid'] = info_.get('columnId')
                            # article_item['topicTitle'] = info_.get('columnId')
                            print('专题')
                            article_item['url'] = info_['contentUrl']
                            self.analyzearticle(article_item)
                #     # break
            elif data['articleType'] == 6:
                pass
            elif data['articleType'] == 4 and data['colID'] == 2134:

                self.analyzearticle_2(article_item, data['contentUrl'])
                break
            elif data['articleType'] == 0:
                article_item['title'] = data['title']
                article_item['author'] = data['arthorName']
                article_item['source'] = data['source']
                article_item['images'] = data.get('pic_list')
                article_item['videoUrl'] = data.get('videoUrl')
                article_item['workerid'] = data['fileId']
                article_item['pubtime'] = data['version']
                article_item['likenum'] = data['countPraise']
                article_item['sharenum'] = data['countShare']
                article_item['commentnum'] = data['countDiscuss']
                article_item['articlecovers'] = data.get('pic_list_title')
                article_item['readnum'] = data.get('countClick')
                article_item['url'] = data['contentUrl']
                self.analyzearticle(article_item)

            # break

    def analyzearticle(self, article_item):
        print(article_item['url'])
        r = self.send_request({
            'url': article_item['url'],
            'headers': headers,
            'method': 'get',
        }).__next__()['request_res']
        # print(r)
        print(article_item['url'])
        data = json.loads(r)
        # print(data)
        article_item['content'] = data['content']
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

    # 特殊新闻
    def analyzearticle_2(self, article_item, url):

        r = self.send_request({
            'url': url,
            'headers': headers,
            'method': 'get',
        }).__next__()['request_res']
        html = etree.HTML(r)
        article_id = html.xpath('string(//div[@class="hide getid"])')
        # print(article_id)
        url_ = f'http://qc.wa.news.cn/nodeart/list?nid={article_id}&pgnum=1&cnt=10&attr=63&tp=1&orderby=1'
        r_ = self.send_request({
            'url': url_,
            'headers': headers,
            'method': 'get',
        }).__next__()['request_res']
        datas = json.loads(r_[1:-1])
        for data in datas['data']['list']:
            article_item['title'] = data['Title']
            article_item['author'] = data['Author']
            article_item['source'] = data['SourceName']
            article_item['images'] = data.get('allPics')
            article_item['workerid'] = data['DocID']
            article_item['pubtime'] = data['PubTime']
            article_item['url'] = data['LinkUrl']
            r_article = self.send_request({
                'url': data['LinkUrl'],
                'headers': headers,
                'method': 'get',
            }).__next__()['request_res']
            html_article = etree.HTML(r_article)
            article_item['content'] = html_article.xpath('string(/html/body/div[3]/div[2]/div/div[2])')
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
        for l in channel_urls:
            print(l)
            self.analyze_articlelists(l)


if __name__ == '__main__':
    gzrb = GuangZhouRiBao('广州日报')
    gzrb.run()
