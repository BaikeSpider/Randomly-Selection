# coding:utf-8
import urllib.request
import urllib.error


class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        try:
           response = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
           print(e.code)
           # print(e.read().decode('utf-8'))
           return None

        if (response.getcode() != 200):
            return None
        return response.read()

