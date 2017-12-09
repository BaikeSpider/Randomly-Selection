# Randomly-Selection

## PREREQUISITES

Python3.6；
ipdb；
pandas；
bs4

## INTRODUCTION
The crawler is composed by two parts, one is producing random links, the other one is crawling the data, including titles, links degree count, edit times, number of editors, total pageviews and create time of entries.
 

#### I. The first part

1. Run the spider_main.py
2. The program will write down the random link into two files, "baidu_result.txt" and "wiki_result.txt".

Note: The spider_main.py will try to produce the links by random number. It produce the random number firstly, and then examine the validity of the link (for example 'https://baike.baidu.com/view/21018707) and catch the title of this entry. If the same title¡¯s entry existed in Wikipedia, the program will write down this result into the files(baidu_result.txt and wiki_result.txt). 


#### II. The secord part

1. Run the baidu_crawl.py and wiki_crawl.py respectively. They will read "baidu_result.txt" and "wiki_result.txt".
2. The crawling results can be found in "baidu_output.xlsx" and "wiki_output.xlsx"

## LICENSE
This program is free tools: you can redistribute it and/or modify it under the terms of MIT License as published.
