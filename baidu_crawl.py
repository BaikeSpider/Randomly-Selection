import url_manager, html_downloader, baidu_parser, baidu_outputer
from bs4 import BeautifulSoup
import urllib
from urllib.parse import urljoin


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.baidu_parser = baidu_parser.HtmlParser()
        self.outputer = baidu_outputer.HtmlOutputer()


    def craw(self):
        urls = []
        baiduentries = open("baidu_result.txt", encoding='utf-8')
        # existentries.write('crawl failed ')
        # baiduentries.write('%s' % ii)
        # baiduentries.write('\n')
        count = 0
        for line in baiduentries:
            urls.append(line)
            count = count + 1
        baiduentries.close()
        i = 0
        self.outputer.output_randomhtml_init()
        while i < count:
            baidu_html_cont = self.downloader.download(urls[i])
            baidu_soup = BeautifulSoup(baidu_html_cont, 'html.parser')
            title = baidu_soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
            baidu_new_titles, baidu_keyword_times, baidu_new_data, baidu_urls, titles_len, history_link, edits, pageviews, contributors_count, time2 = self.baidu_parser.parse(urls[i], baidu_soup)
            self.outputer.output_txt(title.text, baidu_new_data)
            self.outputer.collect_keyword(baidu_urls, baidu_new_titles, urls[i], baidu_keyword_times)
            self.outputer.output_html(title.text)
            self.outputer.output_randomhtml(title.text, urls[i], titles_len, history_link, edits, pageviews, contributors_count, time2)
            i = i+1
        self.outputer.output_randomhtml_finish()

if __name__=='__main__':

    baidu = SpiderMain()
    baidu.craw()
