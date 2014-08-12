import os
from operator import itemgetter
import urllib2,urllib
from xml.dom.minidom import parseString
import time,socket

def safeData(s):
    data = ''
    bReturn =1
    while bReturn<5:
        try:
            user_agent = 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.10) Gecko/20100915 Ubuntu/10.04 (lucid) Firefox/3.6.10'
            request = urllib2.Request(s)
            request.add_header('User-agent', user_agent )
            data = urllib2.urlopen(request).read()
            bReturn = 5
        except:
            bReturn +=1
            time.sleep(1)
            continue
    return data