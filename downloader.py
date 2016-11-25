# coding:utf8
from urllib import request
import os
import json
import sys

class Downloader(object):
    # 显示下载进度
    def _cb(self,blocknum, blocksize, totalsize):
        '''回调函数
        @blocknum: 已经下载的数据块
        @blocksize: 数据块的大小
        @totalsize: 远程文件的大小
        '''
        percent = 100.0 * blocknum * blocksize / totalsize
        if percent > 100:
            percent = 100
        # 格式化输出下载进度,不需要换行
        sys.stdout.write("'[%.2f%%]  \r" % (percent))
        # 让下载百分比再同一行不断刷新
        sys.stdout.flush()

    # 获取指定url请求返回的响应
    def _get_response(self,url):
        if url is None:
            return None

        req = request.Request(url)
        # 模拟火狐浏览器
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0')
        response = request.urlopen(req)
        if response.status != 200:
            return None
        return response.read().decode('utf-8')

    # 获取指定id对应的url
    def get_url_from_id(self,id):
        # {"result": 0, "data": {"result": {"mid": 6687, "mpath": [
        #     "http:\/\/v2.mukewang.com\/e849a994-0ca1-4e6f-a73c-57437a3fb2e7\/L.mp4?auth_key=1479972233-0-0-cf38a3c69532b41284b2de63738eb359",
        #     "http:\/\/v2.mukewang.com\/e849a994-0ca1-4e6f-a73c-57437a3fb2e7\/M.mp4?auth_key=1479972233-0-0-3b4d5d716f474a9d33dda9b364c2dd8e",
        #     "http:\/\/v2.mukewang.com\/e849a994-0ca1-4e6f-a73c-57437a3fb2e7\/H.mp4?auth_key=1479972233-0-0-9248ccde9e7471bb5bb19a1196cc71e8"],
        #                                   "cpid": "1689", "name": "Node.js\u57fa\u7840-\u524d\u8a00", "time": 0,
        #                                   "practise": []}}, "msg": "\u6210\u529f"}
        url = 'http://www.imooc.com/course/ajaxmediainfo/?mid='+id+'&mode=flash'
        # 返回的是string化的json数据
        res=self._get_response(url)
        # json.load载入后为dict数据
        dict_data = json.loads(res)
        # 返回高清视频对应的url
        return dict_data['data']['result']['mpath'][2]

    # 下载指定url对应的html
    def download_html(self,url):
        return self._get_response(url)

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
        request.urlretrieve(url, addr,self._cb)