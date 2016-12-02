# coding:utf8
class UrlManager():
    # 初始化UrlManager维护的两个set
    def __init__(self):
        self._urls = set()
        # self.old_urls = set()

    # 添加单个url
    def add_url(self, url):
        if url is None:
            return
        if url not in self._urls:
            self._urls.add(url)

    # 添加一组url
    def add_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_url(url)
    # 判断是否有新的url
    def has_url(self):
        return len(self._urls) != 0

    def get_url(self):
        url = self._urls.pop()  # pop会从集合删除并返回一个元素
        # if url not in self.old_urls:
        # self.old_urls.add(url)
        return url


        # def v2tov1(self):
    #     pass