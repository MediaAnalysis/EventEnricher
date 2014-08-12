import os
import threading

class globalconfig:
    def __init__(self,flickrAPI,flickrSecret, tmpdir,histbin,outputdir, metadatadir,logdir, maxN):
        self.tmpdir = tmpdir  #dir for the photos and features
        self.histbin = histbin  #exe file to extract features from photos
        self.outputdir = outputdir  #dir for the output xml file
        self.flickrAPI = flickrAPI  #flickrAPI
        self.flickrSecret = flickrSecret  #flickrAPI secret
        self.metadatadir = metadatadir   #dir for the query meta data
        self.logdir = logdir
        dirs = [tmpdir,outputdir,metadatadir,logdir]
        for d in dirs:
        	if not os.path.exists(d):
        		os.makedirs(d)
        self.maxN = maxN

flickrAPIKey = "1ac426232a99179b2055e0fec4acc7fc"  # API key
flickrSecret = "c40aee258fb3ff03"                  # shared "secret"
gconfig = globalconfig(flickrAPIKey,flickrSecret,'photo','hist.exe','result','metadata','log',200)

lockertime = threading.RLock()
lockerdir = threading.RLock()


        