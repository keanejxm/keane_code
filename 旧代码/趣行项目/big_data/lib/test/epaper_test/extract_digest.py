# -*- coding:utf-8 -*-
"""
# project:
# author: Neil
# date: 2020/12/23
# update: 2020/12/23
"""

import re
import html
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
        r = re.compile(r'''<iframe.*?</iframe>''', re.I | re.M | re.S)
        s = r.sub('', s)
        return s

    @staticmethod
    def remove_empty_line(contents):
        """remove multi space """
        assert contents and isinstance(contents, str), "Error param, content."
        r = re.compile(r'''^\s+$''', re.M | re.S)
        s = r.sub('', contents)
        r = re.compile(r'''\n+''', re.M | re.S)
        s = r.sub('\n', s)
        return s

    def remove_any_tag_but_a(self, s):
        """
        匹配a标签中的内容
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

    def extract(self, contents, k=1):
        """
        操作content
        :param contents:
        :param k:
        :return:
        """
        assert contents and isinstance(contents, str), "Error param, content."
        contents = self.remove_empty_line(self.remove_js_css(contents))
        if not contents:
            return None, None, None, None
        tmp = contents.split('\n')
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
                        text_b = "".join(text_b.split()).replace("a", "").strip()
                        content = unicodedata.normalize('NFKC', text_b)
                        digest = content[:200]
                    else:
                        text_b = "".join(text_b.split()).strip()
                        content = unicodedata.normalize('NFKC', text_b)
                        digest = content[:200]
                else:
                    continue
            except Exception as e:
                raise Exception(e)
        return digest, temp


# if __name__ == '__main__':
#     content = '<div class="main-aticle">&#13;\n<p align="center"><iframe class="pageVideo" height="360" marginheight="0" src="https://player.v.news.cn/api/v1/getPlayPage?uuid=1_1a20e72966714fc295a9d816818dc691&amp;vid=d5c2d98718d2d2a83f7f6e673a93af98&amp;playType=0" frameborder="0" width="640" marginwidth="0" scrolling="no" allowfullscreen="true" allowscriptaccess="always" video_height="360" video_width="640" video_src="https://vodpub1.v.news.cn/original/20201225/4d87c3207cf3407e8db4319b79dfe5d1.mp4" vid="d5c2d98718d2d2a83f7f6e673a93af98" uuid="1_1a20e72966714fc295a9d816818dc691" filelength="3451200000" filesize="91462212.0"> </iframe></p>&#13;\n<p style="TEXT-ALIGN: center" align="center">  环境就是民生</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">青山就是美丽</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">蓝天也是幸福</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">2020年</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">总书记多次在考察调研中</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">强调生态文明建设的重要性</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">年终岁尾</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">让我们循着习近平总书记的足迹</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">感受那山那水</p>&#13;\n<p align="center"><img id="{FBE47807-22F0-4337-B62D-DF4C27C23412}" title="" style="HEIGHT: 203px; WIDTH: 360px" border="0" src="1210946921_16088663944361n.gif" sourcedescription="编辑提供的本地文件" sourcename="本地文件"/></p>&#13;\n<p style="TEXT-ALIGN: center" align="center"><strong><font color="blue">山水林田湖草是生命共同体</font></strong></p>&#13;\n<p style="TEXT-ALIGN: center" align="center">冬日的昆明阳光明媚</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">在滇池北岸的星海半岛生态湿地一期</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">工人们正忙着修剪枝叶</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">这里目前已成为远近闻名的网红“打卡地”</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">云南把生态环境保护放在更加突出位置</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">滇池水质整体逐步趋稳</p>&#13;\n<p align="center"><img id="{16E0B3E7-D7F9-4B7F-8D83-2931797A199A}" title="" style="HEIGHT: 203px; WIDTH: 360px" border="0" src="1210946921_16088664160801n.gif" sourcedescription="编辑提供的本地文件" sourcename="本地文件"/></p>&#13;\n<p style="TEXT-ALIGN: center" align="center"><strong><font color="blue">保护生态就是发展生产力</font></strong></p>&#13;\n<p style="TEXT-ALIGN: center" align="center">在浙江余村</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">潘春林自己开办的农家乐生意红火</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">2020年，余村加快了建设步伐</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">“两山”理念指引中国经济社会绿色变革</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">已成为全社会的共识和行动</p>&#13;\n<p align="center"><img id="{CF8541B0-2E03-4BE3-BDF2-8211F0B18693}" title="" style="HEIGHT: 203px; WIDTH: 360px" border="0" src="1210946921_16088664405261n.gif" sourcedescription="编辑提供的本地文件" sourcename="本地文件"/></p>&#13;\n<p style="TEXT-ALIGN: center" align="center"><strong><font color="blue">人不负青山，青山定不负人</font></strong></p>&#13;\n<p style="TEXT-ALIGN: center" align="center">牛背梁国家级自然保护区位于秦岭东段</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">2020年前三季度</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">柞水县空气优良天数同比增加19天</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">生态环境质量持续向好</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">秦岭生态安全屏障更加牢固</p>&#13;\n<p align="center"><img id="{B053FEB5-5F04-4F1D-81FC-8336F39183E1}" title="" style="HEIGHT: 203px; WIDTH: 360px" border="0" src="1210946921_16088664646041n.gif" sourcedescription="编辑提供的本地文件" sourcename="本地文件"/></p>&#13;\n<p style="TEXT-ALIGN: center" align="center">一山一水、一草一木</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">习近平总书记时时牵挂在心</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">绿水长流、青山常在、空气常新</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">正生动绘出美丽中国、幸福家园的模样</p>&#13;\n<p align="center"><img id="{50552FF8-96CB-4667-9708-C71CCF26134D}" title="" style="HEIGHT: 203px; WIDTH: 360px" border="0" src="1210946921_16088664869931n.gif" sourcedescription="编辑提供的本地文件" sourcename="本地文件"/></p>&#13;\n<p align="center">\xa0</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">策划：孙承斌</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">出品人：孙志平</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">监制：樊华</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">统筹：李杰 王健</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">编导：田甜</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">记者：孙敏、王怿文、李涛、陈昌奇、麦凌寒、刘彪（实习）</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">报道员：江波、陶高旸、董越</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">配音：王若凡（实习）</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">新华社音视频部制作</p>&#13;\n<p style="TEXT-ALIGN: center" align="center">新华通讯社出品</p>&#13;\n</div>&#13;'
#     GetExtractDigest().extract(content)