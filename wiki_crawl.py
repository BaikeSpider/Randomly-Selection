import url_manager, html_downloader, wiki_parser, wiki_outputer
from bs4 import BeautifulSoup
import urllib
from urllib.parse import urljoin


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.wiki_parser = wiki_parser.HtmlParser()
        self.outputer = wiki_outputer.HtmlOutputer()


    def craw(self):
        urls = []
        titles = []
        wikientries = open("wiki_result.txt", encoding='utf-8')
        # existentries.write('crawl failed ')
        # baiduentries.write('%s' % ii)
        # baiduentries.write('\n')
        count = 0
        for line in wikientries:
            if count % 2 == 0:
                line1 = line.strip()
                titles.append(line1)
            else:
                line1 = line.strip()
                urls.append(line1)
            count = count + 1
        wikientries.close()
        i = 0
        self.outputer.output_randomhtml_init()
        while i < count / 2:
            wiki_html_cont = self.downloader.download(urls[i])
            wiki_soup = BeautifulSoup(wiki_html_cont, 'html.parser')

            wiki_new_titles, wiki_keyword_times, wiki_new_data, wiki_urls, titles_len, edits, pageviews_url, editors, first_edit, totalviews = self.wiki_parser.parse(urls[i], wiki_soup)
            self.outputer.output_txt(titles[i], wiki_new_data)
            self.outputer.collect_keyword(wiki_urls, wiki_new_titles, urls[i], wiki_keyword_times)
            self.outputer.output_html(titles[i])
            self.outputer.output_randomhtml(titles[i], urls[i], titles_len, pageviews_url, edits, editors, first_edit, totalviews)
            i = i+1
        self.outputer.output_randomhtml_finish()

if __name__=='__main__':

    wiki = SpiderMain()
    wiki.craw()
