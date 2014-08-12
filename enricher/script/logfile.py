
import datetime
import os

class logger():
    def __init__(self,fname):
        self.fname = fname
        if os.path.exists(fname):
            os.remove(fname)
    def info(self,msg):
        t = datetime.datetime.now()
        fw = open(self.fname,'a')
        fw.write('%s %s\n' % (t.strftime("%d/%m/%Y %H:%M"),msg))
        fw.close()
