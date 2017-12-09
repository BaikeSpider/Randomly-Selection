# coding:utf-8
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from urllib.parse import quote
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
        return new_titles, keyword_times, new_urls

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
        # url
        # res_data['url'] = page_url
        
        title_node = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
        parent_title = title_node.get_text()
        res_data['title'] = parent_title
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
        return res_data

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


    def parse(self, baidu_url, wiki_url, baidu_soup, wiki_soup):
        #if page_url is None or html_cont is None:
        #    return
        # soup = BeautifulSoup(html_cont, 'html.parser')
        # print(soup.prettify())
        baidu_new_titles, baidu_keyword_times, baidu_urls = self._baidu_get_new_urls(baidu_url, baidu_soup)
        wiki_new_titles, wiki_keyword_times, wiki_urls = self._wiki_get_new_urls(wiki_url, wiki_soup)
        baidu_new_data = self._baidu_get_new_data(baidu_url, baidu_soup)
        wiki_new_data = self._wiki_get_new_data(wiki_url, wiki_soup)
        # print('mark')
        return baidu_new_titles, baidu_keyword_times, baidu_new_data, baidu_urls, wiki_new_titles, wiki_keyword_times, wiki_new_data, wiki_urls