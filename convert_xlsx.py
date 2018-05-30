# coding:utf-8
import pandas
import os

if __name__=='__main__':
    filename = "wiki_output (3)"
    with open(filename + ".html", "r", encoding="utf-8") as f:
         ddf = pandas.read_html(f.read())
    # print (df[0])
    b = pandas.ExcelWriter(filename + '.xlsx')
    ddf[0].to_excel(b)
    b.close()