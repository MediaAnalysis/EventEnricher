
from pool import ThreadPool
import os
import urllib

image = urllib.URLopener()

def download(data):
    url = data[0]
    fname = data[1]
    if not os.path.exists(fname):
        bTest = 1
        while bTest<5:
            try:		
                image.retrieve(url,fname)
                break
            except:
                bTest +=1
                continue

class Download():
    def __init__(self, folder):
        self.folder = folder
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.pool = ThreadPool(3)
        
    def download(self, dlist):
        for url in dlist:
            fname = url.split('/')[-1]
            self.pool.queueTask(download,(url,os.path.join(self.folder,fname)))
        self.pool.joinAll()
	