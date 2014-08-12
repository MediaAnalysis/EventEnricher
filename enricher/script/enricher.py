
from flickrquery import Download, FlickrQuery
from eventmedia import eventinfo
from datetime import datetime
from filter import filter
from refine import refine
from getfeature import getfeature

from globalconfig import gconfig
import logfile

def enricher(id):
    query = FlickrQuery(gconfig.flickrAPI,gconfig.flickrSecret)
    event = eventinfo(id)
    logger = logfile.logger(gconfig.logdir + '/%s.txt' % event.id)
    logger.info('query event information')
    if not event.succ:
        logger.info( "can not find such event" )
        return
    logger.info('query photos with machine tag')
    idlist = query.searchbyid(event.id)
    db = Download(gconfig.tmpdir + '/%s' % event.id)
    db.download(idlist)
    #query.outputlist(idlist, event.id, 'list/idlist_%s.txt' % event.id)
    logger.info('query photos with text info')
    titlelist = query.searchbytitle(event.title,event.stime,event.id)
    db.download(titlelist)
    #query.outputlist(titlelist,event.id, 'list/titlelist_%s.txt' % event.id)
    logger.info('query photos with geo info')
    geolist = query.searchbygeo(event.lat,event.lng,event.stime,event.id)
    db.download(geolist)
    #query.outputlist(geolist,event.id,'list/geolist_%s.txt' % event.id)

    logger.info('parsing features')    
    feature = getfeature()
    feature.run(gconfig.tmpdir + '/%s' % event.id)
    
    #trainfile = 'list/idlist_%s.txt' % event.id
    trainlist = []
    for url in idlist:
        fname = url.split('/')[-1]
        fname = gconfig.tmpdir + '/%s' % event.id + '/' + fname
        trainlist.append(fname.replace('.jpg','_ch.txt'))
        
    testlist = []
    for url in titlelist:
        fname = url.split('/')[-1]
        fname = gconfig.tmpdir + '/%s' % event.id + '/' + fname
        testlist.append(fname.replace('.jpg','_ch.txt'))

    logger.info('visual pruning')        
    myfilter = filter(trainlist,testlist)
    r = myfilter.filter()
    lst = []
    for idx in r:
        lst.append(testlist[idx])

    logger.info('refining')        
    myrefine = refine(event.id,lst)
    results = myrefine.refine()
    newresults = query.geturlbyid(results,titlelist)

    logger.info('output result')    
    query.OutputXML(event.id,idlist,titlelist,geolist,newresults)
    query.OutputHtml(event.id,idlist,titlelist,geolist,newresults)
    logger.info('event-finished')    

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        id = (sys.argv[1])
    else:
        id = 'http://data.linkedevents.org/event/0a385594-5e9f-44c9-98f5-d56bc15aaf07'
    enricher(id)
