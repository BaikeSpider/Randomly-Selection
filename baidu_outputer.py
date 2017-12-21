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
    def collect_keyword(self, baidu_new_urls, baidu_new_titles, baidu_url, baidu_keyword_times):
        ii = 0
        jj = 0
        self.baidu_keywords = []
        while ii < len(baidu_new_urls):
            res_keyword = {}
            res_keyword['url'] = baidu_new_urls[ii]
            res_keyword['title'] = baidu_new_titles[ii]
            res_keyword['id'] = ii + 1
            res_keyword['parent_url'] = baidu_url
            res_keyword['keyword_time'] = baidu_keyword_times[ii]
            # res_keyword['parent_all'] = parent_all
            self.baidu_keywords.append(res_keyword)
            ii = ii+1

    def output_txt(self, title, baidu_data):
        if not (os.path.isfile('txt/'+'baidu_'+title+'.txt')):
           fout = open('txt/'+'baidu_'+title+'.txt','w', encoding='utf-8')
           fout.write(baidu_data['title'])
           fout.write('\n')
           fout.write(baidu_data['summary'])
           fout.close()
        else:
           fout = open('txt/'+'_baidu_'+title+'.txt','w',  encoding='utf-8')
           fout.write(baidu_data['title'])
           fout.write('\n')
           fout.write(baidu_data['summary'])
           fout.close()
           record = open('baidu_samekeywords.txt','a',encoding='utf-8')
           #record.write(new_data['parent'])
           record.write(baidu_data['title'])
           record.write('\n')
           record.close()


    def output_html(self, title, users, users_edits):
        # set_trace()
        if not (os.path.isfile("html/"+'baidu_'+title+'_intext.html')):
           filename = 'baidu_'+title
        else:
           filename = '_baidu_'+title
           
        fout = open("html/"+filename+'_intext.html','w', encoding='utf-8')
        fout.write('<html>')
        fout.write('<body>')
        fout.write('<table>')

        for keyword in self.baidu_keywords:
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
        if len(self.baidu_keywords):
            with open("html/"+filename+'_intext.html','r',encoding='utf-8') as f:  
               df = pandas.read_html(f.read()) 
        # print (df[0])  
            bb = pandas.ExcelWriter("xlsx/"+filename+'_intext.xlsx')  
            df[0].to_excel(bb) 
            bb.close()

        # save the editors history
        filename2 = "baidu_" + title
        fout = open("baidu_history/"+filename2+".html",'w', encoding='utf-8')
        fout.write('<html>')
        fout.write('<body>')
        fout.write('<table>')
        ii = 0
        while ii< len(users):
            fout.write('<tr>')
            fout.write('<td>%s</td>' % users[ii])
            fout.write('<td>%s</td>' % users_edits[ii])
            fout.write('</tr>')
            ii += 1
        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
        fout.close()
        if ii > 0:
            with open("baidu_history/"+filename2+".html", "r", encoding= "utf-8") as f:
               ddf = pandas.read_html(f.read())
        # print (df[0])
            b2 = pandas.ExcelWriter("baidu_history_xlsx/"+ filename2+'.xlsx')
            ddf[0].to_excel(b2)
            b2.close()

    def output_randomhtml_init(self):
        filename = 'baidu_output'
        fout = open(filename + '.html', 'w', encoding='utf-8')
        fout.write('<html>')
        fout.write('<body>')
        fout.write('<table>')
        fout.close()

    def output_randomhtml(self, title, link, degree, history_link, edits, pageviews, contributors_count, time2, all_len, category, reference_count):
        # set_trace()
        filename = 'baidu_output'

        fout = open(filename + '.html', 'a', encoding='utf-8')
        fout.write('<tr>')
        fout.write('<td>%s</td>' % title)
        fout.write('<td>%s</td>' % link)
        fout.write('<td>%s</td>' % degree)
        fout.write('<td>%s</td>' % history_link)
        fout.write('<td>%s</td>' % edits)
        fout.write('<td>%s</td>' % contributors_count)
        fout.write('<td>%s</td>' % time2)
        fout.write('<td>%s</td>' % pageviews)
        fout.write('<td>%s</td>' % reference_count)
        fout.write('<td>%s</td>' % all_len)
        html_str = ""
        for jj in category:
            html_str = html_str + jj
            html_str = html_str + ","
        fout.write('<td>%s</td>' % html_str)
        fout.write('<td>%s</td>' % len(category))
        # fout.write('<td>%s</td>' % parent_all)
        # fout.write('<td>%s</td>' % parent_all.count('_'))
        fout.write('</tr>')
        # set_trace()
        fout.close()

    def output_randomhtml_finish(self):
        filename = 'baidu_output'
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


'''
    def output_dataset(self, users_dataset, index_dataset):
        filename = "baidu_users"
        fout = open(filename + '.html', 'w', encoding='utf-8')
        fout.write('<html>')
        fout.write('<body>')
        fout.write('<table>')
        ii = 0
        for id in index_dataset:
            fout.write('<tr>')
            fout.write('<td>%s</td>' % users_dataset[id]['uname'])
            fout.write('<td>%s</td>' % users_dataset[id]['portraitUrl'])
            fout.write('<td>%s</td>' % users_dataset[id]['experience'])
            fout.write('<td>%s</td>' % users_dataset[id]['level'])
            fout.write('<td>%s</td>' % users_dataset[id]['commitTotalCount'])
            fout.write('<td>%s</td>' % users_dataset[id]['commitPassedCount'])
            fout.write('<td>%s</td>' % users_dataset[id]['createPassedCount'])
            fout.write('<td>%s</td>' % users_dataset[id]['goodVersionCount'])
            fout.write('<td>%s</td>' % users_dataset[id]['featuredLemmaCount'])
            fout.write('<td>%s</td>' % users_dataset[id]['passRatio'])
            fout.write('<td>%s</td>' % users_dataset[id]['isTeamOdp'])
            fout.write('</tr>')
        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
        fout.close()
        with open(filename + ".html", "r", encoding= "utf-8") as f:
            ddf = pandas.read_html(f.read())
        # print (df[0])
        b = pandas.ExcelWriter(filename + '.xlsx')
        ddf[0].to_excel(b)
        b.close()
'''
