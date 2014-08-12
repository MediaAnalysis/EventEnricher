import numpy as np
import math
from refine import  refine
from getfeature import getfeature

class filter():
    def __init__(self,trainlist,testlist):
        self.trainlist = trainlist
        self.testlist = testlist
    def L1_abs(self,v,t):
        sum = 0
        for ii in range(len(t)):
            sum += math.fabs(v[ii]-t[ii])
        return sum
        
    def filter(self):
        results= []
        feature = []
        testdata = []
        for f in self.trainlist:
            try:
                v = np.loadtxt(f)
                feature.append(v)
            except:
                continue
        for f in self.testlist:
            try:
                v = np.loadtxt(f)
                testdata.append(v)
            except:
                continue
        N = len(feature)
        for i in range(N):
            v = feature[i]
            th = 1
            for j in range(N):
                if j == i:
                    continue
                t = feature[j]
                sum = self.L1_abs(v,t)
                if th>sum:
                    th = sum
            N2 = len(testdata)
            for j in range(N2):
                t = testdata[j]
                sum = self.L1_abs(v,t)
                if sum<th:
                    results.append(j)
        return results
		 
        