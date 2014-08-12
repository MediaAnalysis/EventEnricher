import os
from enricher import enricher
from globalconfig import gconfig,lockerdir

from flickrquery import  FlickrQuery
from downloader import Download
from eventmedia import eventinfo
from datetime import datetime
from filter import filter
from refine import refine
from getfeature import getfeature
import json
import time

query = FlickrQuery(gconfig.flickrAPI,gconfig.flickrSecret)

def ReadData(fname):
        json_file = open(fname)
        data = json.load(json_file)
        json_file.close()
        return data

def LoadEventInfo(url):
        event = eventinfo(url)
        strdata = json.dumps(event.__dict__)
        id = event.id

        d = gconfig.metadatadir + '/%s' % id
        fname = gconfig.metadatadir + '/%s/info.json' % id
        lockerdir.acquire()
        if not os.path.exists(d):
                os.makedirs(d)
        lockerdir.release()

        jsonfile = open(fname,'w')
        jsonfile.write(strdata)
        jsonfile.close()
        return event.__dict__

def QueryPhotobyId(id):
    fname = gconfig.metadatadir + '/%s/id.json' % id
    if os.path.exists(fname):
        return ReadData(fname)
    else:
        idlist = query.searchbyid(id)

        idtable = query.OutputJson(idlist)
        strdata = json.dumps(idtable)
        jsonfile = open(fname,'w')
        jsonfile.write(strdata)
        jsonfile.close()
        return idtable

def QueryPhotobyTitle(id,title,stime):
    fname = gconfig.metadatadir + '/%s/title.json' % id
    if os.path.exists(fname):
        return ReadData(fname)
    else:
        titlelist = query.searchbytitle(title,stime,id)

        ttable = query.OutputJson(titlelist)
        strdata = json.dumps(ttable)
        jsonfile = open(fname,'w')
        jsonfile.write(strdata)
        jsonfile.close()
        return ttable

    
def QueryPhotobyGeo(id,geo,stime):
    fname = gconfig.metadatadir + '/%s/geo.json' % id
    if os.path.exists(fname):
        return ReadData(fname)
    else:
        lat = geo[0]
        long = geo[1]
        geolist = query.searchbygeo(lat,long,stime,id)
        
        gtable = query.OutputJson(geolist)
        strdata = json.dumps(gtable)
        jsonfile = open(fname,'w')
        jsonfile.write(strdata)
        jsonfile.close()
        return gtable

def downloadAll(id):
    keys = ['geo','id','title']
    dlist = []
    for k in keys:
        fname = gconfig.metadatadir + '/%s/%s.json' % (id,k)
        fr = open(fname)
        data = json.loads(fr.read())
        for photo in data['photos']:
            dlist.append(photo['photo'])
        fr.close()
            
    db = Download(gconfig.tmpdir + '/%s' % id)
    db.download(dlist)

def WaitAll(id):
    keys = ['geo','id','title']
    for k in keys:
        fname = gconfig.metadatadir + '/%s/%s.json' % (id,k)
        while(not os.path.exists(fname)):
            time.sleep(5)

def QueryFinalPhotos(id):
    ffname = gconfig.metadatadir + '/%s/final.json' % id
    if os.path.exists(ffname):
        return ReadData(ffname)
    else:
        WaitAll(id)
        downloadAll(id)
        
        fname = gconfig.metadatadir + '/%s/id.json' % id
        if not os.path.exists(fname):
            QueryPhotobyId(id)
        
        tmp = ReadData(fname)
        idlist = [t['photo'] for t in tmp['photos']]

        event = LoadEventInfo('http://data.linkedevents.org/event/' + id)
        tmp = event['stime'].split('T')[0]
        stime = datetime.strptime(tmp,'%Y-%m-%d')
        
        fname = gconfig.metadatadir + '/%s/title.json' % id
        if not os.path.exists(fname):
            QueryPhotobyTitle(id,event['title'],stime)

        tmp = ReadData(fname)
        titlelist = [t['photo'] for t in tmp['photos']]
        print "titlelist", len(titlelist)

        fname = gconfig.metadatadir + '/%s/geo.json' % id
        if not os.path.exists(fname):
            QueryPhotobyGeo(event['id'],(event['lat'],event['lng']),stime)
            
        tmp = ReadData(fname)
        geolist = [t['photo'] for t in tmp['photos']]
        
        trainlist = []
        for url in idlist:
            fname = url.split('/')[-1]
            fname = gconfig.tmpdir + '/%s' % id + '/' + fname
            trainlist.append(fname.replace('.jpg','_ch.txt'))
            
        testlist = []
        alldata = titlelist + geolist
        
        for url in alldata:
            fname = url.split('/')[-1]
            fname = gconfig.tmpdir + '/%s' % id + '/' + fname
            testlist.append(fname.replace('.jpg','_ch.txt'))
        
        feature = getfeature()
        feature.run(gconfig.tmpdir + '/%s' % id)
    
        myfilter = filter(trainlist,testlist)
        r = myfilter.filter()  #return the index in testing data
        lst = []
        for idx in r:
            lst.append(testlist[idx])
        print "the number of pruned is %d" % len(lst)
        myrefine = refine(id,lst)
        results = myrefine.refine()
        
        newresults = query.geturlbyid(results,alldata)
        ftable = query.OutputJson(idlist + newresults)
        
        strdata = json.dumps(ftable)
        jsonfile = open(ffname,'w')
        jsonfile.write(strdata)
        jsonfile.close()
        return ftable