#-*- coding: utf-8 -*-

from ipdb import set_trace
import pandas
import os

def conertit(filename, count) :
       df = pandas.read_excel(path+"/"+filename,
                       sheetname='Sheet1',
                       header=0)
       # l = len(df)
       # i = 0
       #line = line('utf-8')
       #line4 = [1]*2500
       line = df.loc[0,7]

       #while i<l:
        #  line4[i] = df.loc[i,4]
        #  line4[i] = str(line4[i])
          # if (line4[i] not in old_node) and (type(line4[i]) is type('a')):
             # node_group.append(line4[i])
        #  i = i+1

       if line>3:
         os.remove(path+"/"+filename)
         print(filename)
         fout = open('xlsx_deleted_list.txt','a', encoding='utf-8')
         fout.write(filename)
         fout.write('\n')
         fout.close()
         count = count + 1
       return count
       # columnlen = 8
       # cc = 0
       #while cc < columnlen:
       #  df[cc].to_excel(bb)
       #  cc = cc + 1

       #set_trace()



if __name__=='__main__':
    file_init = '政治'
    ii = 0
    path = "G:/Python/Baidu-Spider/Encyclopedia_Poject/Baidu-new/xlsx-verity"
    node_group = os.listdir(path)
    #old_node = set()
    count = 0
    while ii<len(node_group):

      file_init = node_group[ii]
      # if file_init not in old_node:
      if os.path.splitext(file_init)[1] == '.xlsx' and os.path.isfile(path + "/" + file_init):
          try:
           print(file_init, '---now')
           # set_trace()
           count = conertit(file_init, count)
           # old_node.add(file_init)
          except:
           fout = open('xlsx_failed_record.txt','a', encoding='utf-8')
           fout.write(file_init)
           fout.write('\n')
           fout.close()
      ii = ii +1
    print(count)

