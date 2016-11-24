# coding:utf8
from urllib import request
import os

class Downloader(object):

    # 下载指定url对应的html
    def download_html(self,url):
        if url is None:
            return None

        req=request.Request(url)
        # 模拟火狐浏览器
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0')
        response=request.urlopen(req)
        if response.status!=200:
            return None
        return response.read()

    # 下载指定url对应的mp4
    def download_mp4(self, url,name,course_name):
        # 获得当前目录
        current_dir = os.getcwd()
        # 当前工作目录下新建课程目录
        course_dir = os.path.join(current_dir, course_name)
        if (not os.path.exists(course_dir)):
            os.mkdir(course_dir)
        # 创建视频保存地址
        addr= os.path.join(course_dir, name+ '.mp4')
        # 下载url地址对应的视频到课程目录下，并以视频的名称命名
        request.urlretrieve(url, addr)