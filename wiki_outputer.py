# coding:utf-8
import pandas
import os
from ipdb import set_trace 

class HtmlOutputer(object):
    def __init__(self):
        self.datas = []
        # self.keywords = []
    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def collect_keyword(self, wiki_new_urls, wiki_new_titles, wiki_url, wiki_keyword_times):
        ii = 0
        jj = 0
        self.wiki_keywords = []
        while ii < len(wiki_new_urls):
            res_keyword = {}
            res_keyword['url'] = wiki_new_urls[ii]
            res_keyword['title'] = wiki_new_titles[ii]
            res_keyword['id'] = ii + 1
            res_keyword['parent_url'] = wiki_url
            res_keyword['keyword_time'] = wiki_keyword_times[ii]
            # res_keyword['parent_all'] = parent_all
            self.wiki_keywords.append(res_keyword)
            ii = ii+1

    def output_txt(self, title, wiki_data):
        if not (os.path.isfile('txt/'+'wiki_'+title+'.txt')):
           fout = open('txt/'+'wiki_'+title+'.txt','w', encoding='utf-8')
           fout.write(wiki_data['title'])
           fout.write('\n')
           fout.write(wiki_data['summary'])
           fout.close()
        else:
           fout = open('txt/'+'_wiki_'+title+'.txt','w',  encoding='utf-8')
           fout.write(wiki_data['title'])
           fout.write('\n')
           fout.write(wiki_data['summary'])
           fout.close()
           record = open('wiki_samekeywords.txt','a',encoding='utf-8')
           #record.write(new_data['parent'])
           record.write(wiki_data['title'])
           record.write('\n')
           record.close()


    def output_html(self, title):
        # set_trace()
        if not (os.path.isfile("html/"+"wiki_"+ title+"_intext.html")):
           filename = "wiki_" + title
        else:
           filename = "_wiki_" + title
           
        fout = open("html/"+filename+"_intext.html",'w', encoding='utf-8')
        fout.write('<html>')
        fout.write('<body>')
        fout.write('<table>')

        for keyword in self.wiki_keywords:
            fout.write('<tr>')
            fout.write('<td>%s</td>' % title)
            fout.write('<td>%s</td>' % keyword['parent_url'])
            fout.write('<td>%s</td>' % keyword['id'])
            fout.write('<td>%s</td>' % keyword['url'])
            fout.write('<td>%s</td>' % keyword['title'])
            fout.write('<td>%s</td>' % keyword['keyword_time'])
            #fout.write('<td>%s</td>' % parent_all)
            #fout.write('<td>%s</td>' % parent_all.count('_'))
            fout.write('</tr>')
        # set_trace()
        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
        fout.close()
        if len(self.wiki_keywords):
            with open("html/"+filename+"_intext.html", "r", encoding= "utf-8") as f:
               df = pandas.read_html(f.read()) 
        # print (df[0])  
            bb = pandas.ExcelWriter("xlsx/"+filename+'_intext.xlsx')  
            df[0].to_excel(bb)
            bb.close()

    def output_randomhtml_init(self):
        filename = "wiki_output"
        fout = open(filename + ".html", "w", encoding="utf-8")
        fout.write('<html>')
        fout.write('<body>')
        fout.write('<table>')
        fout.close()

    def output_randomhtml(self, title, link, degree, pageviews_url, edits, editors, first_edit, totalviews):
        # set_trace()
        filename = 'wiki_output'

        fout = open(filename + '.html', 'a', encoding='utf-8')
        fout.write('<tr>')
        fout.write('<td>%s</td>' % title)
        fout.write('<td>%s</td>' % link)
        fout.write('<td>%s</td>' % degree)
        fout.write('<td>%s</td>' % pageviews_url)
        fout.write('<td>%s</td>' % edits)
        fout.write('<td>%s</td>' % editors)
        fout.write('<td>%s</td>' % first_edit)
        fout.write('<td>%s</td>' % totalviews)
        # fout.write('<td>%s</td>' % parent_all)
        # fout.write('<td>%s</td>' % parent_all.count('_'))
        fout.write('</tr>')
        # set_trace()
        fout.close()

    def output_randomhtml_finish(self):
        filename = 'wiki_output'
        fout = open(filename + '.html', 'a', encoding='utf-8')
        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
        fout.close()
        with open(filename + '.html', 'r', encoding='utf-8') as f:
             df = pandas.read_html(f.read())
                # print (df[0])
        bb = pandas.ExcelWriter(filename + '.xlsx')
        df[0].to_excel(bb)
        bb.close()