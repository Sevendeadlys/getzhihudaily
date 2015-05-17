#!/usr/bin/env python
# encoding: utf-8

import requests
import os
import sys
import re
import time

getid = lambda x:re.search(r'(\d+)',x).group(1)

class dailydown:
    def __init__(self):
        self.root = "http://daily.zhihu.com"
        self.header = {'Accept':r'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', \
                'Accept-Encoding':'gzip, deflate', \
                'Accept-Language':'en-US,en;q=0.5', \
                'Host':'daily.zhihu.com', \
                'User-Agent':r'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:32.0) Gecko/20100101 Firefox/32.0',\
                'Referer':r'http://daily.zhihu.com/', \
                'Cache-Control':r'max-age=0', \
                'Connection':r'keep-alive', \
                }
        self.oldlist = []

    def init_list(self):
        try:
            req = requests.get(self.root,headers=self.header)
            if req.status_code == 200:
                #print req.content
                self.get_url(req.content)
                #print self.get_title(req.content)

            for url in self.urllist:
                urlid = getid(url)
        except Exception:
            print "init list error"

    def init_dir(self):
        self.urllist = []
        try:
            pwd = os.getcwd()
            reportdir = pwd + r'/data'
            if not os.path.exists(reportdir):
                os.mkdir(reportdir)

            oldurllist = pwd + r'/oldlist.txt'
            if os.path.exists(oldurllist):
                f = open(oldurllist,'r')
                for line in f.readlines():
                    line = line.strip()
                    if not line :
                        continue
                    else:
                        self.oldlist.append(line.strip())
                f.close()
                print self.oldlist
        except:
            print "init dir error"

    def get_useful_content(self,html):
        reg = re.compile(r'<div class\=\"box\">(.+?)<\/div>',re.I|re.M)
        try:
            for match in reg.finditer(html):
               yield  match.group(1)
        except:
            print 'content error'

    def get_url(self,html):
        reg = re.compile(r'<[^<>]+?href=\"([^<>]+?)\"[^<>]+?>',re.I|re.M)
        try:
            for content in self.get_useful_content(html):
                match = reg.search(content)
                if not match:
                    continue
                else:
                    self.urllist.append(match.group(1))
            #print self.urllist
        except:
            print 'get url error'

    def get_html(self,url):
        try:
            print url
            req = requests.get(url,self.header)
            print req.content
            if req.status_code == 200:
                return req.content
        except:
            print 'get html error'

    def get_title(self,html):
        try:
            reg = re.compile(r'<title>(.+?)<\/title>',re.I|re.M)
            htmlname = reg.search(html).group(1)
        except:
            print 'html name error'
        return htmlname

    def store_html(self,html):
        try:
            pwd = os.getcwd()
            htmlname = self.get_title(html)
            htmlname += r'.html'
            htmlname = pwd + r'\/data\/'+htmlname
            f = open(htmlname,'w+')
            f.write(html)
            f.close()
        except:
            print 'store html error'


    def get_daily(self):
        try:
            for url in self.urllist:
                urlid = getid(url)
                print urlid
                html = self.get_html(url)
                self.store_html(html)
        except:
            print 'daily error'



    def main(self):
        self.init_dir()
        self.init_list()
        self.get_daily()


if __name__=='__main__':
    p = dailydown()
    p.main()
