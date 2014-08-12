

from safeData import safeData
import re
import datetime
from xml.dom.minidom import parseString
import socket
socket.setdefaulttimeout(90)


class eventinfo():
    def __init__(self,id):
        self.id = id
        self.geteventinfo(id)
    def setinfo(self,tags,lat,long,stime,etime):
        self.tags = tags
        self.lat = lat
        self.lng = long
        self.stime = datetime.datetime.strptime(stime,'%Y-%m-%d')
        self.etime = datetime.datetime.strptime(etime,'%Y-%m-%d')
        
    def geteventinfo(self,id):
        s= 'http://ws.audioscrobbler.com/2.0/?method=event.getinfo&event=%s&api_key=ad9b2d3b791541cd4ae8c2088224bb14' % id
        self.succ = 0
        data = safeData(s)
        try:
            xdata = parseString(data)
        except:
            return
            
        t = xdata.getElementsByTagName('title')
        self.title = t[0].childNodes[0].nodeValue
        
        t = xdata.getElementsByTagName('startDate')
        time = t[0].childNodes[0].nodeValue

        t = xdata.getElementsByTagName('venue')
        vid = t[0].getElementsByTagName('name')
        vid = vid[0].childNodes[0].nodeValue
        self.venue = vid
        
        t = xdata.getElementsByTagName('city')
        if t[0].childNodes:
            self.city = t[0].childNodes[0].nodeValue
        
        t = xdata.getElementsByTagName('geo:lat')
        if t[0].childNodes:
            self.lat = float(t[0].childNodes[0].nodeValue)
        else:
            self.lat = ''
        t = xdata.getElementsByTagName('geo:long')
        if t[0].childNodes:
            self.lng = float(t[0].childNodes[0].nodeValue)
            self.succ = 1
        else:
            self.lng = ''
            self.succ = 0
    def printf(self):
        print self.id,self.title,self.lat,self.lng,self.stime,self.city
