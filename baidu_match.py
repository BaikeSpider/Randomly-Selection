# -*- coding: utf-8 -*-

import pandas
import os


class SpiderMain(object):

    def check_branch(self, branch,title1):
        count0 = 0
        for jj in branch:
            key = jj.strip()
            if title1 == key:
                count0 += 1             
        return count0
        
    def check1(self, title, j):
          if title == '政治':    
            df.loc[:, '12'][j] = 1
          else:
            count1 = self.check_branch(branch1, title)
            if count1>0:
               df.loc[:, '13'][j] += count1
            else:
               count1 = self.check_branch(branch2, title)
               if count1 > 0:
                   df.loc[:, '14'][j] += count1
               else:
                   count1 = self.check_branch(branch3, title)
                   if count1 > 0:
                      df.loc[:, '15'][j] += count1

    def match(self):
        # input the list
        count = 0
        global branch1
        branch1 = []
        branch_txt = open("baidu_branch1.txt", encoding='utf-8')
        for line in branch_txt:
            branch1.append(line)
            count = count + 1
        branch_txt.close()
        print('input branch1:', count)
        count = 0
        global branch2
        branch2 = []
        branch_txt = open("baidu_branch2.txt", encoding='utf-8')
        for line in branch_txt:
            branch2.append(line)
            count = count + 1
        branch_txt.close()
        print('input branch2:', count)
        count = 0
        global branch3
        branch3 = []

        branch_txt = open("baidu_branch3.txt", encoding='utf-8')
        for line in branch_txt:
            branch3.append(line)
            count = count + 1
        branch_txt.close()
        print('input branch3:', count)
        count = 0
        # input the randomly selected entries list
        
        global df
        df = pandas.read_excel('baidu_output.xlsx',
                       sheet_name='Sheet1',
                       header=0)
        l = len(df)
        i = 0
        templist = []
        while i<l:
           templist.append(0)
           i += 1
        i = 0
        df['8'] = templist
        df['9'] = templist
        df['10'] = templist
        df['11'] = templist
        df['12'] = templist
        df['13'] = templist
        df['14'] = templist
        df['15'] = templist
        while i<l:
          title = df[0][i]
          filename = 'baidu_' + title + '_intext.xlsx'
          if title == '政治':
            df.loc[:, '8'][i] = 1
            df.loc[:, '9'][i] = 0
            df.loc[:, '10'][i] = 0
            df.loc[:, '11'][i] = 0
          else:
            count1 = self.check_branch(branch1, title)
            if count1 >0:
              df.loc[:, '8'][i] = 0
              df.loc[:, '9'][i] = count1
              df.loc[:, '10'][i] = 0
              df.loc[:, '11'][i] = 0
            else:
              count1 = self.check_branch(branch2, title)
              if count1 >0:
                df.loc[:, '8'][i] = 0
                df.loc[:, '9'][i] = 0
                df.loc[:, '10'][i] = count1
                df.loc[:, '11'][i] = 0
              else:
                count1 = self.check_branch(branch3, title)
                if count1 >0:
                  df.loc[:, '8'][i] = 0
                  df.loc[:, '9'][i] = 0
                  df.loc[:, '10'][i] = 0
                  df.loc[:, '11'][i] = count1
                else:
                  df['8'][i] = 0
                  df['9'][i] = 0
                  df.loc[:, '10'][i] = 0
                  df.loc[:, '11'][i] = 0
          if os.path.isfile("xlsx/" + filename):
            dff = pandas.read_excel("xlsx/" + filename,
                       sheet_name='Sheet1',
                       header=0)          
            ll = len(dff)
            ii = 0
            while ii<ll:
               if dff[5][ii] <= 0:
                   ii +=1
                   continue
               title2 = dff[4][ii]
               self.check1(title2, i)
               ii += 1
          i += 1
          bb = pandas.ExcelWriter('baidu_output.xlsx')
          df.to_excel(bb)
          bb.close()


if __name__=='__main__':

    baidu = SpiderMain()
    baidu.match()
