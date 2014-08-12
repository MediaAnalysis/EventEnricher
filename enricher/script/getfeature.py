# -*- coding: utf-8 -*-
import os,sys,time
import re
import subprocess

class getfeature():
    def eachfile(self,filename):
        jpg = filename.replace('/','\\')
        chfile = jpg.replace('.jpg','_CH.txt')
        if not os.path.exists(jpg):
            return
        if not os.path.exists(chfile):
             cmd = 'hist.exe \"%s\"' % jpg
             startupinfo = subprocess.STARTUPINFO()
             startupinfo.dwFlags |= _subprocess.STARTF_USESHOWWINDOW
             subprocess.Popen(cmd, startupinfo=startupinfo).wait()
    def runcmd(self,cmd):
             startupinfo = subprocess.STARTUPINFO()
             startupinfo.dwFlags |= _subprocess.STARTF_USESHOWWINDOW
             subprocess.Popen(cmd, startupinfo=startupinfo).wait()
    def runsift(self,dir):
        cmd = './lip-vireo -dir %s -d dog -p SIFT -dsdir %s -c config.txt' % (dir,dir)
        self.runcmd(cmd)
        self.convert(dir)
    def convertfile(self,filename):
        try:
            f = open(filename)
        except:
            return
        data = f.readlines()
        f.close()
        newfile = filename.replace('pkeys','key')
        if os.path.exists(newfile):
            return
        f1 = open(newfile,'w')
        num = len(data)
        for idx in range(2,num,12):
            str = ''
            for i in range(0,11):
                str  = str + data[idx+i].strip() + ' '
            f1.write(str+'\n')
        f1.close()
        
    def convert(self,dir):
        files = os.listdir(dir)
        for filename in files:
            if filename.find('pkeys')>0:
                self.convertfile(dir + filename)
                
    def run(self,dirs):
        for lstfile in os.listdir(dirs):
            if lstfile.find('.jpg')>0:
                    self.eachfile(dirs + '/' + lstfile.strip())
        self.runsift(dirs)
		

