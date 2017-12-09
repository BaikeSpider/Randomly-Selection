# coding:utf-8
import url_manager, html_downloader, html_parser, html_outputer
import random
from bs4 import BeautifulSoup
import urllib
from urllib.parse import urljoin
from ipdb import set_trace


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, times):

        ii = 0
        baidu_page_url = 'https://baike.baidu.com/view/21018707'
        wiki_page_url = 'https://zh.m.wikipedia.org/zh-cn/%E5%9C%B0%E7%90%86%E5%A4%A7%E7%99%BC%E7%8F%BE'
        while ii < times:
            baidu_new_url = random.randint(1, 21061500)
            # baidu_new_url = 19012282
            baidu_new_url = str(baidu_new_url)+'.htm'
            baidu_full_url = urljoin(baidu_page_url, baidu_new_url)
            baidu_html_cont = self.downloader.download(baidu_full_url)
            if  baidu_html_cont == None:
                continue
            if baidu_html_cont == b'':  # something wrong in the judgement above, so judge again to avoid the error
                continue
            baidu_soup = BeautifulSoup(baidu_html_cont, 'html.parser')
            # print(baidu_new_url)
            if baidu_soup.find('p',class_ ="sorryCont") != None:
                # print("sorryCont", baidu_full_url)
                continue
            title = baidu_soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
            wiki_new_url = urllib.parse.quote(title.text)
            wiki_full_url = urljoin(wiki_page_url, wiki_new_url)
            # set_trace()
            wiki_html_cont = self.downloader.download(wiki_full_url)
            if wiki_html_cont == None:
                noexistentries = open("noexistedentries2.txt", 'a', encoding='utf-8')
                noexistentries.write('crawl failed ')
                noexistentries.write('%s' % ii)
                noexistentries.write('\n')
                noexistentries.write(baidu_full_url)
                noexistentries.write('\n')
                noexistentries.write(wiki_full_url)
                noexistentries.write('\n')
                noexistentries.close()
                continue
            else:
                baiduentries = open("baidu_result2.txt", 'a', encoding='utf-8')
                baiduentries.write(baidu_full_url)
                baiduentries.write('\n')
                baiduentries.close()
                wikientries = open("wiki_result2.txt", 'a', encoding='utf-8')
                wikientries.write(title.text)
                wikientries.write('\n')
                wikientries.write(wiki_full_url)
                wikientries.write('\n')
                wikientries.close()


if __name__=='__main__':
    times = 500
    obj_spider = SpiderMain()
    obj_spider.craw(times)
