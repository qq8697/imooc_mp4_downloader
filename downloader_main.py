# coding:utf8
'''
    思路:
    1. 用户输入课程id,得到课程url地址,启动下载器。
    2. 下载并解析课程url,返回视频url列表，放在set中。
        TODO 1,set要求是可哈希的，视频的名字如何和视频url关联？
        set({'url':'aa','name':'bb'},{'url':'ab','name':'bc'})-->set expected at most 1 arguments, got 2
        set([{'url':'aa','name':'bb'},{'url':'ab','name':'bc'}])-->unhashable type: 'dict'
        -->返回一个dict以url为key，name为value,同时返回url组成的列表
            get_name={'aa':'bb'}
            mp4_lists=['aa','ab']
        TODO 2,为什么非要放在set中？
        -->配合try except实现断点续传
    3. 下载mp4视频
'''
# 添加当前目录到path
import sys
import os
sys.path.append(os.path.split(os.getcwd())[0])
from moocmp4_downloader import url_manager, downloader, html_parser, html_outputer
from datetime import datetime

class Downloader_Main(object):
    # 初始化函数
    def __init__(self):
        # 初始化url管理器
        self.urls = url_manager.UrlManager()
        # 初始化下载器
        self.downloader = downloader.Downloader()
        # 初始化解析器
        self.parser = html_parser.HtmlParser()
        # 初始化输出器
        self.outputer = html_outputer.HtmlOutputer()

    # 下载课程
    def download(self, course_num):
        # 计时器
        start = datetime.now()
        # 得到课程编号对应的root_url
        root_url = 'http://www.imooc.com/learn/' + course_num
        # 下载课程即root_url对应的html
        html_cont = self.downloader.download_html(root_url)
        # 解析课程html返回mp4列表、url列表和课程名称
        mp4_lists,urls,course_name = self.parser.parse(html_cont)
        # 添加urls到url管理器
        self.urls.add_urls(urls)
        # url管理器非空,执行以下循环
        while self.urls.has_url():
            # 获取新的url
            url = self.urls.get_url()
            # 输出待爬取的url
            print('下载:%s，地址为:%s' % (mp4_lists[url],url))
            try:
                # 下载url对应的视频
                self.downloader.download_mp4(url,mp4_lists[url],course_name)
            except:
                print('%s下载失败，重新下载'% mp4_lists[url])
                self.urls.add_url(url)
        # 输出html页面
        self.outputer.output(mp4_lists,course_name)
        print('共用时：', (datetime.now() - start + datetime(1970, 1, 1)).strftime('%H:%M:%S'))

if __name__ == '__main__':
    # 得到课程编号
    course_num = input('请输入课程id...')
    # 实例化下载器
    downloader = Downloader_Main()
    # 下载指定课程
    downloader.download(course_num)
