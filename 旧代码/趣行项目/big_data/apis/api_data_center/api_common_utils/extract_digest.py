# -*- coding:utf-8 -*-
"""
# project:
# author: Neil
# date: 2020/12/23
# update: 2020/12/23
"""
import html
import re
import unicodedata


class GetExtractDigest:

    @staticmethod
    def remove_js_css(contents):

        """ remove the the javascript and the stylesheet and the comment content (<script>....</script> and <style>....
        </style> <!-- xxx -->) """
        assert contents and isinstance(contents, str), "Error param, content."
        contents = html.unescape(contents)
        contents = html.unescape(contents)
        contents = unicodedata.normalize('NFKC', contents).replace("\n", "").replace("\t", "").replace("\r", "")
        r = re.compile(r'''<script.*?</script>''', re.I | re.M | re.S)
        s = r.sub('', contents)
        r = re.compile(r'''<style.*?</style>''', re.I | re.M | re.S)
        s = r.sub('', s)
        r = re.compile(r'''<!--.*?-->''', re.I | re.M | re.S)
        s = r.sub('', s)
        r = re.compile(r'''<meta.*?>''', re.I | re.M | re.S)
        s = r.sub('', s)
        r = re.compile(r'''<ins.*?</ins>''', re.I | re.M | re.S)
        s = r.sub('', s)
        return s

    @staticmethod
    def remove_empty_line(content):
        """remove multi space """
        assert content and isinstance(content, str), "Error param, content."
        r = re.compile(r'''^\s+$''', re.M | re.S)
        s = r.sub('', content)
        r = re.compile(r'''\n+''', re.M | re.S)
        s = r.sub('\n', s)
        return s

    def remove_any_tag_but_a(self, s):
        """
        匹配a标签中的内容并移除a标签之外的内容
        :param s: content
        :return:
        """
        text = re.findall(r'''<a[^r][^>]*>(.*?)</a>''', s, re.I | re.S | re.S)  # 匹配a标签中的内容
        text_b = re.sub(r'''<[^>]+>''', '', s)
        return len(''.join(text)), text_b

    @staticmethod
    def remove_image(s, n=100):
        image = 'a' * n
        if "<img" in s:
            r = re.compile(r'''<img.*?>''', re.I | re.M | re.S)
            s = r.sub(image, s)
        elif "<image" in s:
            r = re.compile(r'''<image.*?>''', re.I | re.M | re.S)
            s = r.sub(image, s)
        else:
            return s
        return s

    @staticmethod
    def remove_video(s, n=1000):
        video = 'a' * n
        if "<embed" in s:
            r = re.compile(r'''<embed.*?>''', re.I | re.M | re.S)
            s = r.sub(video, s)
        elif "<video" in s:
            r = re.compile(r'''<video.*?>''', re.I | re.M | re.S)
            s = r.sub(video, s)
        else:
            return s
        return s

    def extract(self, content, k=1):
        """
        操作content
        :param content:
        :param k:
        :return:
        """
        assert content and isinstance(content, str), "Error param, content."
        content = self.remove_empty_line(self.remove_js_css(content))
        if not content:
            return None, None, None, None
        tmp = content.split('\n')
        digest = ""
        temp = 0
        for i in range(0, len(tmp), k):
            try:
                group = '\n'.join(tmp[i:i + k])
                if group:
                    group = self.remove_image(group)
                    group = self.remove_video(group)
                    text_a, text_b = self.remove_any_tag_but_a(group)
                    temp = (len(text_b) - text_a) - 8  # content字数
                    if "a" in text_b:
                        text_b = "".join(text_b.split()).replace("a", "").strip().replace("  ", "")
                        content = str(unicodedata.normalize('NFKC', text_b)).strip()
                        digest = content[:200]
                    else:
                        text_b = "".join(text_b.split()).strip().replace("  ", "")
                        content = str(unicodedata.normalize('NFKC', text_b)).strip()
                        digest = content[:200]
                else:
                    continue
            except Exception as e:
                raise Exception(e)
        return digest, temp
