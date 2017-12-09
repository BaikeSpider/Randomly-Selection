# coding:utf-8
from bs4 import BeautifulSoup
import re
import html_downloader
import requests
import json
from urllib.parse import urljoin
from urllib.parse import quote
from urllib.request import urlopen
from ipdb import set_trace 

class HtmlParser(object):
    def replaceillgalchar(self, link_text):
        # set_trace()
        while link_text.find(':')>=0:
          # 
          link_text = link_text.replace(':', '-')
        while link_text.find('?')>=0:
          link_text = link_text.replace('?', '-')
        while link_text.find('<')>=0:
          link_text = link_text.replace('<', '-')
        while link_text.find('>')>=0:
          link_text = link_text.replace('>', '-')
        while link_text.find('|')>=0:
          link_text = link_text.replace('|', '-')       
        while link_text.find(r'\\')>=0:
          link_text = link_text.replace(r'\\', '-')  
        while link_text.find('\/')>=0:
          # set_trace()
          link_text = link_text.replace(r'\/', '-')  
        return link_text
        
    def _baidu_get_new_urls(self, page_url, soup):
        new_urls = []
        new_titles = []
        keyword_times = []
        # /view/123.htm
        # links = soup.find_all('a', href=re.compile(r'/view/[\u4e00-\u9fa5]+'))
        links = soup.find_all('a',href=re.compile(r'/item/*'))
        old_link = set()
        for link in links:
            if link.text not in old_link:
               new_url = link['href']
               if new_url != '/item/史记·2016?fr=navbar':
                   new_full_url = urljoin(page_url, new_url)
                   # print(new_full_url)
                   new_urls.append(new_full_url)
                   if link.get('title') != None:
                     if (link['title'] != ''):
                        textnow = self.replaceillgalchar(link['title'])
                     else:
                        textnow = self.replaceillgalchar(link.text)         
                   else:
                      textnow = self.replaceillgalchar(link.text)        
                   
                   new_titles.append(textnow) 
                   old_link.add(link.text)
                   temp = link.text
                   if (temp.find('(') != -1):
                     temp = temp.replace('(','\(')
                   if (temp.find(')') != -1):
                     temp = temp.replace(')','\)')  
                   if (temp.find('+') != -1):
                     temp = temp.replace('+','\+')  
                   if (temp.find('*') != -1):
                     temp = temp.replace('*','\*')
                   if (temp.find(' ') != -1):
                     temp = temp.replace(' ','\s')
                   if (temp.find('?') != -1):
                     temp = temp.replace('?','\?')
                   if (temp.find('[') != -1):
                     temp = temp.replace('[','\[')
                   if (temp.find(']') != -1):
                     temp = temp.replace(']','\]')
                   if (temp.find('{') != -1):
                     temp = temp.replace('{','\{')
                   if (temp.find('}') != -1):
                     temp = temp.replace('}','\}')
                   keyword_time = soup.find_all(string=re.compile(temp))
                   keywordtime = 0
                   for keyword in keyword_time:
                      keywordtime = keywordtime + keyword.count(link.text)
                   keyword_times.append(keywordtime)
     
        #print(new_urls)
        # set_trace()
        return len(new_titles), new_titles, keyword_times, new_urls

    def _wiki_get_new_urls(self, page_url, soup):
        # def has_class_and_text(tag):
        #   return tag['class'] == 'references'
        # def has_class_but_no_id(tag):
        #   return tag.has_attr('class')
        new_urls = []
        new_titles = []
        keyword_times = []
        # /view/123.htm
        # links = soup.find_all('a', href=re.compile(r'/view/[\u4e00-\u9fa5]+'))
        # set_trace()
        links_orginal = soup.find_all('a', href=re.compile(r'/wiki/'))
        links = []
        illegalchar = ('*', '+', '-', '?', '.', ',')
        deleurl1 = re.compile(r'/wiki/Special:')
        deleurl2 = re.compile(r'/wiki/Category:')
        deleurl3 = re.compile(r'/wiki/%E7%BB%B4%E5%9F%BA%E8%AF%AD%E5%BD%95')
        deleurl4 = re.compile(r'/wiki/Wikipedia:')
        deleurl5 = re.compile(r'/wiki/File:')
        deleurl6 = re.compile(r'/wiki/Template:')
        deleurl7 = re.compile(r'/wiki/Portal:')
        deleurl8 = re.compile(r'/wiki/Privacy_policy')
        deleurl9 = re.compile(r'/wiki/%E7%BB%B4%E5%9F%BA%E5%85%B1%E4%BA%AB%E8%B5%84%E6%BA%90')
        deleurl10 = re.compile(r'/wiki/Help:')
        deleurl11 = re.compile(r'wiktionary\.org')
        deleurl12 = re.compile(r'wikimediafoundation\.org')
        deleurl13 = re.compile(r'wikivoyage\.org')
        deleurl14 = re.compile(r'wikimedia\.org')
        deleurl17 = re.compile(r'wikisource\.org')
        deleurl18 = re.compile(r'wikidata\.org')
        deleurl19 = re.compile(r'wikibooks\.org')
        deleurl15 = re.compile(r'/wiki/Main_Page')
        deleurl16 = re.compile(r'/wiki/Talk:')
        convert = re.compile(r'zh.m.wikipedia\.org/wiki/')

        for link in links_orginal:
            #if re.search('\.(jpg|JPG|svg|SVG)$',link['href']):
            #    links.remove(link)
            if not ((re.search(deleurl1, link['href'])) or (re.search(deleurl2, link['href'])) or (
            re.search(deleurl3, link['href'])) or (re.search(deleurl4, link['href'])) or (
            re.search(deleurl6, link['href'])) or (re.search(deleurl5, link['href'])) or (
            re.search(deleurl7, link['href'])) or (re.search(deleurl8, link['href'])) or (
            re.search(deleurl9, link['href'])) or (re.search(deleurl10, link['href'])) or (
            re.search(deleurl11, link['href'])) or (re.search(deleurl12, link['href'])) or (
            re.search(deleurl13, link['href'])) or (re.search(deleurl14, link['href'])) or (
            re.search(deleurl15, link['href'])) or (re.search(deleurl16, link['href'])) or (
            re.search(deleurl17, link['href'])) or (re.search(deleurl18, link['href'])) or (re.search(deleurl19, link['href']))) :
                links.append(link)
        old_link = set()
        # set_trace()
        for link in links:
            if link.text == '':
                continue
                # print(link) # for test

                # if link['href'] == '/wiki/%E6%97%A5%E8%AA%9E%E6%9B%B8%E5%AF%AB%E7%B3%BB%E7%B5%B1':
                # set_trace()

            if link['href'].find('#') != -1:
                t = link['href'].find('#')
                link['href'] = link['href'][0:t]
            # link.text = Converter('zh-hans').convert(link.text )  # transform the text
            if link.text not in old_link:
                new_url = link['href']
                new_full_url = urljoin(page_url, new_url)
                if re.search(convert, new_full_url):
                   new_full_url = new_full_url.replace('/wiki/', '/zh-cn/')
                # set_trace()
                new_urls.append(new_full_url)
                # if 'title' in link):
                if link.get('title') != None:
                    if (link['title'] != ''):
                        textnow = self.replaceillgalchar(link['title'])
                    else:
                        textnow = self.replaceillgalchar(link.text)
                else:
                    textnow = self.replaceillgalchar(link.text)
                new_titles.append(textnow)
                old_link.add(link.text)

                temp = link.text
                if (temp.find('(') != -1):
                    temp = temp.replace('(', '\(')
                if (temp.find(')') != -1):
                    temp = temp.replace(')', '\)')
                if (temp.find('+') != -1):
                    temp = temp.replace('+', '\+')
                if (temp.find('*') != -1):
                    temp = temp.replace('*', '\*')
                if (temp.find(' ') != -1):
                    temp = temp.replace(' ', '\s')
                if (temp.find('?') != -1):
                    temp = temp.replace('?', '\?')
                keyword_time = soup.find_all(string=re.compile(temp))
                keywordtime = 0
                for keyword in keyword_time:
                    keywordtime = keywordtime + keyword.count(link.text)
                keyword_times.append(keywordtime)

        # set_trace()
        return len(new_titles), new_titles, keyword_times, new_urls


    def _baidu_get_new_data(self, page_url, soup):
        res_data = {}
        # res_data['url'] = page_url

        #title
        title_node = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
        parent_title = title_node.get_text()
        res_data['title'] = parent_title
        #summary
        summary_node = soup.find('div', class_='lemma-summary')
        if (summary_node != None): 
          if (summary_node.get_text() != None):
            res_data['summary'] = summary_node.get_text()
          else:
            res_data['summary'] = '!!!No summary!!!'     
        else:
          res_data['summary'] = '!!!No summary!!!'        
        # res_data['parent'] = parent
        # print(res_data)

        #histroy_link
        history_link = soup.find(class_='nslog:1021')
        history_link = urljoin(page_url, history_link['href'])
        #edits
        edits1 = soup.find(class_='nslog:1021').parent
        edits2 = edits1.text
        pos = edits2.rfind('次')
        edits = edits2[5: pos]
        #pageviews
        pos = 0
        string2 = 'error'
        temp1 = soup.find_all('script')
        for ii in temp1:
           string = ii.text
           if string.find('newLemmaIdEnc') != -1:
              string2 = string
              pos = string.find('newLemmaIdEnc')
              break
        #print(result)
        pos = pos + 15
        if string2 == 'error':
            print('error_pageviews', page_url)
            pageviews = 0
        else:
            pageviews_id = string2[pos: pos+24]
            pageviews_url = 'https://baike.baidu.com/api/lemmapv?id=' + pageviews_id
            self.downloader = html_downloader.HtmlDownloader()
            html_cont = self.downloader.download(pageviews_url)
            html_cont = str(html_cont, encoding = "utf-8")
            pos1 = html_cont.find(':')+1
            pos2 = len(html_cont)-1
            pageviews = html_cont[pos1: pos2]

        return res_data, history_link, edits, pageviews

    def _wiki_get_new_data(self, page_url, soup):
        res_data = {}
        # url
        # res_data['url'] = page_url
        title_node = soup.find('div', class_='mw-body').find('h1')
        parent_title = title_node.get_text()
        res_data['title'] = parent_title
        # summary
        summary_node = soup.find(name='p')
        if (summary_node != None):
            if (summary_node.get_text() != None):
                res_data['summary'] = summary_node.get_text()
            else:
                res_data['summary'] = '!!!No summary!!!'
        else:
            res_data['summary'] = '!!!No summary!!!'
        # res_data['parent'] = parent_all
        # print(res_data)

        info_link = soup.find_all('a', href=re.compile(r'&action=info'))
        info_url = urljoin(page_url, info_link[0]['href'])
        self.downloader = html_downloader.HtmlDownloader()
        html_cont = self.downloader.download(info_url)
        info_soup = BeautifulSoup(html_cont, 'html.parser')

        articleinfo_url_temp = info_soup.find_all('a',href=re.compile(r'//tools.wmflabs.org/xtools-articleinfo/index.php'))
        articleinfo_url = 'https:' + articleinfo_url_temp[0]['href']  # https://tools.wmflabs.org/xtools-articleinfo/index.php?article=%E9%98%BF%E7%B1%B3%E4%BB%80%E4%BA%BA&project=zh.wikipedia.org
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        articleinfo_cont = requests.get(articleinfo_url, headers=headers)
        articleinfo_soup = BeautifulSoup(articleinfo_cont.text, 'html.parser')
        text1 = articleinfo_soup.find_all('div', class_='col-lg-6 stat-list clearfix')
        edits = text1[0].find_all('td')[7].text
        edits = edits.strip()
        edits = edits.rstrip()
        # edits= int(edits)  # remove spaces
        editors = text1[0].find_all('td')[9].text
        editors = editors.strip()
        editors = editors.rstrip()

        first_edit = text1[1].find_all('td')[1].text
        pos1 = first_edit.find(',')
        first_edit = first_edit[0: pos1].lstrip()
        # articleinfo_cont = self.downloader.download(articleinfo_url)
        # articleinfo_soup = BeautifulSoup(articleinfo_cont, 'html.parser')

        pos1 = articleinfo_url_temp[0]['href'].find('article=')
        pos2 = articleinfo_url_temp[0]['href'].find('project=')
        entry_title = articleinfo_url_temp[0]['href'][pos1+8: pos2-1]
        #  = info_soup.find_all('a',href=re.compile(r'//tools.wmflabs.org/pageviews'))
        pageviews_url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/zh.wikipedia/all-access/all-agents/' + entry_title + '/daily/2000110100/2017112000'
        # pageviws_cont = requests.get(pageviws_url, headers=headers)
        # pageviws_soup = BeautifulSoup(pageviws_cont.text, 'html.parser', from_encoding='utf-8')

        u = requests.get(pageviews_url, headers=headers)
        # u = urlopen(pageviews_url)
        response = json.loads(u.text)
        totalviews = 0
        for jj in response['items']:
           totalviews += jj['views']

        # pageviws_cont = self.downloader.download(pageviws_url)
        # pageviws_soup = BeautifulSoup(pageviws_cont, 'html.parser')
        # text2 = pageviws_soup.find('div', class_='legend-block--body')

        return res_data,edits, pageviews_url, editors, first_edit, totalviews

    def parse(self, wiki_url, wiki_soup):
        #if page_url is None or html_cont is None:
        #    return
        # soup = BeautifulSoup(html_cont, 'html.parser')
        # print(soup.prettify())
        titles_len, wiki_new_titles, wiki_keyword_times, wiki_urls = self._wiki_get_new_urls(wiki_url, wiki_soup)
        # wiki_new_titles, wiki_keyword_times, wiki_urls = self._wiki_get_new_urls(wiki_url, wiki_soup)
        wiki_new_data, edits, pageviews_url, editors, first_edit, totalviews = self._wiki_get_new_data(wiki_url, wiki_soup)
        # wiki_new_data = self._wiki_get_new_data(wiki_url, wiki_soup)
        # print('mark')
        return wiki_new_titles, wiki_keyword_times, wiki_new_data, wiki_urls, titles_len, edits, pageviews_url, editors, first_edit, totalviews

