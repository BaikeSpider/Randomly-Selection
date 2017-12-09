# coding:utf-8
from ipdb import set_trace


class UrlManager(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
        self.new_urlsgroup = []
        self.parent_urls = []
        self.titles = []
        self.parent_title = []
        self.parent_all = []

    def add_new_urls(self, urls, new_titles, parent_url, parent_title, parent_all):
        if urls is None or len(urls) == 0:
            return
        url_len = len(urls)
        j = 0
        while j < url_len:
            if urls[j] is None:
                continue
            if urls[j] not in self.new_urls and urls[j] not in self.old_urls:
                self.new_urls.add(urls[j])
                self.new_urlsgroup.append(urls[j])
                self.titles.append(new_titles[j])
                self.parent_urls.append(parent_url)
                self.parent_title.append(parent_title)
                self.parent_all.append(parent_all)
            j = j + 1

    def has_new_url(self):
        return len(self.new_urls) != 0

    def recover(self, now_url, title, parent_url, parent_title, parent_all):
        self.old_urls.discard(now_url)
        self.new_urls.add(now_url)
        self.new_urlsgroup.append(now_url)
        self.titles.append(title)
        self.parent_urls.append(parent_url)
        self.parent_title.append(parent_title)
        self.parent_all.append(parent_all)

    def get_new_url(self, now):
        #while self.parent_all[now].count('_') >= 11:
        #    now = now + 1

        new_url = self.new_urlsgroup[now]
        parent_url = self.parent_urls[now]
        title = self.titles[now]
        parent_title = self.parent_title[now]
        parent_all = self.parent_all[now]
        self.old_urls.add(new_url)
        self.new_urls.discard(new_url)
        now = now + 1
        return new_url, title, parent_url, parent_title, parent_all, now
