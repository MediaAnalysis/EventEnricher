from xml.dom.minidom import Document
import xml.parsers.expat
import os
from globalconfig import gconfig
class refine():
    def __init__(self, eid,photos):
        self.eid = eid
        self.photos = photos
        
    def parsexml(self):
        idx  = 1
        photos = {}
        while (1):
            xmlfile = gconfig.metadatadir + '/querybytitle/%s_%d.xml' % (self.eid,idx)
            idx +=1
            if not os.path.exists(xmlfile):
                break
            data = xml.dom.minidom.parse(xmlfile)
            q = data.getElementsByTagName('photo')
            for item in q:
                id = item.getAttribute('id')
                s = item.getAttribute('secret')
                o = item.getAttribute('owner')
                photos[id+'_'+s] =o
        idx = 1 
        while (1):
            xmlfile = gconfig.metadatadir + '/querybygeo/%s_%d.xml' % (self.eid,idx)
            idx +=1
            if not os.path.exists(xmlfile):
                break
            data = xml.dom.minidom.parse(xmlfile)
            q = data.getElementsByTagName('photo')
            for item in q:
                id = item.getAttribute('id')
                s = item.getAttribute('secret')
                o = item.getAttribute('owner')
                photos[id+'_'+s] =o 
        return photos

    def refine(self):
        results = []
        allpid = []
        pid = []
        owners = []
        for p in self.photos:
            p = p.split('/')[-1]
            p = p.replace('_ch.txt','')
            pid.append(p)
        photos = self.parsexml()
        
        for p in pid:
            if p in photos:
                owners.append(photos[p])
        for o in owners:
            for p in photos:
                if o == photos[p]:
                    results.append(p)
        return set(results)

    