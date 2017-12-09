# coding:utf-8
from bs4 import BeautifulSoup
import re
import html_downloader
import requests
from urllib.parse import urljoin
from urllib.parse import quote
from ipdb import set_trace 
from urllib.request import urlopen
import json
import time

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
        return new_titles, keyword_times, new_urls


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


        #histroy_link
        history_link = soup.find(class_='nslog:1021')
        history_link = urljoin(page_url, history_link['href'])
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        u = requests.get(history_link, headers=headers)
        # u = urlopen(history_link)
        history_soup = BeautifulSoup(u.text, 'html.parser')
        result = history_soup.find('script').text
        pos = 0
        string1 = 'error'
        string2 = 'error'
        tk_id = 0
        lemma_id = 0
        edit0 = int(edits)
        pages_num = edit0 // 25
        if edit0 % 25 != 0:
            pages_num += 1
        if result.find('tk') != -1:
            string1 = result
            pos = result.find('tk')
            pos = pos + 16
            tk_id = string1[pos: pos+32]

        else:
            print('error_tk', page_url)

        if result.find('lemmaId') != -1:
            string2 = result
            pos = result.find('lemmaId')
            pos = pos + 15
            pos2 = result.find(';', pos+2)
            lemma_id = string2[pos: pos2]
        else:
            print('error_lemmaId', page_url)

        ii = 1

        dict = {}
        contributors = set()
        contributors_count = 0
        time1 = 9999999999
        while ii<=pages_num:
            history_editlist_url1 = 'https://baike.baidu.com/api/wikiui/gethistorylist?tk=' + tk_id +  '&lemmaId=' + lemma_id
            history_editlist_url2 = '&count=1&size=25'

            history_editlist_url = history_editlist_url1 + '&from=' + str(ii) + history_editlist_url2
            # u = urlopen(history_editlist_url) # seems cannot crawl by this way
            uu = requests.get(history_editlist_url, headers=headers)
            response = json.loads(uu.text)
            # l = response['data']['pages'].len
            j = str(ii)

            for jj in response['data']['pages'][j]:
                 if jj['uid'] not in contributors:
                    contributors_count = contributors_count + 1
                    contributors.add(jj['uid'])
                 if time1 > jj['createTime']:
                    time1 = jj['createTime']
            ii +=1
        time2 = time.strftime("%Y-%m-%d", time.localtime(time1))

        # response = json.loads(u.read().decode('utf-8'))
        # test1 = history_soup.find('div', class_='editedTimes')

        #pageviews_url = 'https://baike.baidu.com/api/lemmapv'
        #params1 = {'id': pageviews_id}
        #response = requests.get(pageviews_url, params=params1)
        #response_text = response.text

        #pos1 = response_text.find(':')+1
        #pos2 = len(response_text)-1
        #pageviews = response_text[pos1: pos2]


        # pageviews = soup.find(id='j-lemmaStatistics-pv')
        # pageviews1 = soup.find(id='j-lemmaStatistics-pv').parent
        # edits = soup.find_next_sibling(id='j-lemmaStatistics-pv')
        # edits = soup.find(class_='nslog:1021')
        # test1 = edits.parent
        # test = soup.find(class_='side-box lemma-statistics')
        # test = soup.find(class_='side-box lemma-statistics').find('li')
        # print(test)
        return res_data, history_link, edits, pageviews, contributors_count, time2

    def _wiki_get_new_data(self, page_url, soup):
        res_data = {}
        # url
        # res_data['url'] = page_url
        title_node = soup.find('div', class_='mw-body').find('h1')
        parent_title = title_node.get_text()
        res_data['title'] = parent_title
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
        return res_data


    def parse(self, baidu_url, baidu_soup):
        #if page_url is None or html_cont is None:
        #    return
        # soup = BeautifulSoup(html_cont, 'html.parser')
        # print(soup.prettify())
        titles_len, baidu_new_titles, baidu_keyword_times, baidu_urls = self._baidu_get_new_urls(baidu_url, baidu_soup)
        # wiki_new_titles, wiki_keyword_times, wiki_urls = self._wiki_get_new_urls(wiki_url, wiki_soup)
        baidu_new_data, history_link, edits, pageviews,  contributors_count, time2 = self._baidu_get_new_data(baidu_url, baidu_soup)
        # wiki_new_data = self._wiki_get_new_data(wiki_url, wiki_soup)
        # print('mark')
        return baidu_new_titles, baidu_keyword_times, baidu_new_data, baidu_urls, titles_len, history_link, edits, pageviews,  contributors_count, time2