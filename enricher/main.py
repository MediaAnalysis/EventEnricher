import web
from web import form

import os
from datetime import datetime
import json
import time

from script.enricher import enricher
from script.globalconfig import gconfig,lockertime

from script.flickrquery import Download, FlickrQuery
from script.eventmedia import eventinfo

from script.filter import filter
from script.refine import refine
from script.getfeature import getfeature
from script.toolkit import *

render = web.template.render('templates/')

urls = ('/', 'index')
app = web.application(urls, globals())

myform = form.Form( 
    form.Textbox("bax",id="search", type="text", placeholder="Type here"),
    )

class index:
    def GET(self): 
        html = open('index.html').readlines()
        return ' '.join(html)

    def POST(self): 
        form = myform() 
        if not form.validates(): 
            return render.formtest(form)
        else:
            tmp = web.input()
            op = tmp['query']
            string = tmp['textfield']
            event = LoadEventInfo(string)
            tmp = event['stime']
            lockertime.acquire()
            stime = datetime.strptime(tmp,'%Y-%m-%dT%H:%M:%SZ')
            lockertime.release()
            
            if op == 'event':
                return json.dumps(event)
            
            if op == 'machinetag':
                print event['id']
                idtable = QueryPhotobyId(event['id'])
                time.sleep(0.5)
                return json.dumps(idtable)

            if op == 'title':
                ttable = QueryPhotobyTitle(event['id'],event['title'],stime)
                time.sleep(1)
                return json.dumps(ttable)
            if op == 'geo':
                gtable = QueryPhotobyGeo(event['id'],(event['lat'],event['lng']),stime)
                time.sleep(1.5)
                return json.dumps(gtable)
            if op == 'final':
                time.sleep(2)
                ftable = QueryFinalPhotos(event['id'])
                return json.dumps(ftable)

if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()