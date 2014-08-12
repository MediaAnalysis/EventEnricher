
from flickrquery import Download, FlickrQuery
from eventmedia import eventinfo
from datetime import datetime
from filter import filter
from refine import refine
from getfeature import getfeature

from globalconfig import gconfig
import logfile

def download():
    query = FlickrQuery(gconfig.flickrAPI,gconfig.flickrSecret)
    lat =  22.38
    lon = 114.11
    radius = 30
    for i in range(1,12):
        stime = '2012-%02d-01' % i
        etime = '2012-%02d-01' % (i+1)
        print stime
        query.searchbygeoRadius(lat,lon,radius, stime, etime, 'hongkong')
##    feature = getfeature()
##    feature.run(gconfig.tmpdir + '/%s' % 'hongkong')
##    

if __name__ == '__main__':
    download()
