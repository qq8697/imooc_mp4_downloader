# coding:utf8
from bs4 import BeautifulSoup
import re
from moocmp4_downloader import downloader

class HtmlParser(object):
    # 初始化函数
    def __init__(self):
        # 初始化下载器
        self.downloader = downloader.Downloader()

    # 将url从v2版改为v1版
    def _v2_to_v1(self,url):
        # http://v2.mukewang.com/e849a994-0ca1-4e6f-a73c-57437a3fb2e7/H.mp4?auth_key=1479972233-0-0-9248ccde9e7471bb5bb19a1196cc71e8
        # http://v1.mukewang.com/e849a994-0ca1-4e6f-a73c-57437a3fb2e7/H.mp4?
        tmp = re.split('\?', url)[0]
        return re.sub('v2','v1',tmp)

    # 获取指定id视频的url的函数
    def _get_mp4_url(self,mp4_id):
        url=self.downloader.get_url_from_id(mp4_id)
        return self._v2_to_v1(url)

    # 获取所有视频url组成的列表和以url为key，name为value组成的mp4的函数
    def _get_urls(self,soup):
        # < a href = "/video/6687" class ="J-media-item" >
        #     < i class ="icon-video type" > < / i >
        #         1 - 1 Node.js基础 - 前言 (01:20)
        selector=soup.find_all('a','J-media-item')
        urls=[]
        mp4={}
        total=len(selector)

        for s in selector:
            # 获取视频id "/video/6687" -->6687
            href=s['href']
            mp4_id=str.replace(href,"/video/",'')
            # 获取text内容        1 - 1 Node.js基础 - 前言 (01:20)
            text=s.get_text()
            # 过滤非视频url,以是否有时间为标准(01:20)
            time_pattern=re.compile('\(\d{2}:\d{2}\)')  # TODO 注意JavaScript和python的正则分别/\(\d{2}:\d{2}\)/和'\(\d{2}:\d{2}\)'
            if(not re.search(time_pattern,text)):
                total=total-1
                if(total==0 ):
                    print("没有视频可以下载！")
                return None

            # 去掉时间，去掉空格，去掉'开始学习'，只留视频名称
            tmp1=re.sub(time_pattern,'',text)
            space_pattern=re.compile('\s*')
            tmp2 = re.sub(space_pattern, '', tmp1)
            mp4_name = re.sub('开始学习', '', tmp2)

            # 获取视频url
            mp4_url=self._get_mp4_url(mp4_id)
            urls.append(mp4_url)
            mp4[mp4_url]=mp4_name
        return mp4,urls

    # 获得课程的名字
    def _get_course_name(self,soup):
        # < div class ="hd clearfix" >
        #     < h2 class ="l" > 进击Node.js基础（一） < / h2 >
        return soup.find_all('h2','l')[0].get_text()

    # 解析课程html，返回视频的url列表以及url为key，name为value组成的mp4 dict以及课程的名字
    def parse(self,html_cont):
        # 得到树形结构的文档对象（传入指定html字符串，解析器以及编码方式）
        soup = BeautifulSoup(html_cont, 'html.parser')
        mp4,urls=self._get_urls(soup)
        course_name=self._get_course_name(soup)

        print(mp4)
        return mp4,urls,course_name