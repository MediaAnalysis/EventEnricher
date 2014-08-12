
from script.flickrquery import Download, FlickrQuery
from script.eventmedia import eventinfo
from datetime import datetime
from script.filter import filter
from script.refine import refine
from script.getfeature import getfeature

from script.globalconfig import gconfig

def enricher(id):
    query = FlickrQuery(gconfig.flickrAPI,gconfig.flickrSecret)
    event = eventinfo(id)
    if not event.succ:
        logger.info( "can not find such event" )
        return
    idlist = query.searchbyid(event.id)
    db = Download(gconfig.tmpdir + '/%s' % event.id)
    db.download(idlist)
    #query.outputlist(idlist, event.id, 'list/idlist_%s.txt' % event.id)
    titlelist = query.searchbytitle(event.title,event.stime,event.id)
    db.download(titlelist)
    #query.outputlist(titlelist,event.id, 'list/titlelist_%s.txt' % event.id)
    geolist = query.searchbygeo(event.lat,event.lng,event.stime,event.id)
    db.download(geolist)
    #query.outputlist(geolist,event.id,'list/geolist_%s.txt' % event.id)

    feature = getfeature()
    feature.run(gconfig.tmpdir + '/%s' % event.id)


if __name__ == '__main__':
    import sys
    for line in open('events.txt'):
        enricher(line.strip())
        