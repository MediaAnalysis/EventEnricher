#!/usr/bin/python

import sys, string, math, time,os,urllib
from flickrapi2 import FlickrAPI
import datetime,socket
from xml.dom.minidom import parseString
import simplejson
from xml.dom.minidom import Document
from globalconfig import gconfig

socket.setdefaulttimeout(90)  


class Download():
	def __init__(self, folder):
		self.folder = folder
	def download(self,photolist):
		self.list = photolist
		image = urllib.URLopener()
		if not os.path.exists(self.folder):
			os.makedirs(self.folder)
		for url in self.list:
			fname = url.split('/')[-1]
			fname = self.folder + '/' + fname
			if not os.path.exists(fname):
				bTest = 1
				while bTest<5:
					try:		
						image.retrieve(url,fname)
						break
					except:
						bTest +=1
						continue

class FlickrQuery():
	def __init__(self,flickrapikey,flickrSecret):
		self.api_key = flickrapikey
		self.fapi = FlickrAPI(flickrapikey, flickrSecret)
	def searchbyid(self,eventid):
		photolist = []
		query = " prefix  lode: <http://linkedevents.org/ontology/> \n\
		prefix	dc: <http://purl.org/dc/elements/1.1/> \n\
		prefix	ma: <http://www.w3.org/ns/ma-ont#> \n\
		SELECT ?event ?eventTitle ?URI \n\
		WHERE { \n\
		?event dc:title ?eventTitle. \n\
		?photo lode:illustrate ?event. \n\
		?photo ma:locator ?URI. \n\
		FILTER (?event = <http://data.linkedevents.org/event/eventURI>). \n\
		}  \n\
		"
		query = query.replace('eventURI',eventid)
		searchbase = 'http://eventmedia.eurecom.fr/sparql'
		params = urllib.urlencode({"format": "application/sparql-results+json", "query": query})
		f = urllib.urlopen(searchbase + '?' + params)
		results = simplejson.load(f)
		try:
			results = results['results']['bindings']
		except:
			return []
		for result in results:
			url = result['URI']['value']
			photolist.append(url)
		return photolist

	def searchbytitle(self,title,time,eventid):
		photolist = []
		t1 = time
		t2 = t1 + datetime.timedelta(days = 5)
		starttime = t1 + datetime.timedelta(hours = - (t1.hour))

		bReturn = 1
		idx = 1
		while (bReturn ==1):
			try:			
				rsp = self.fapi.photos_search(api_key=self.api_key,
										ispublic="1",
										media="photos",
										per_page="250", 
										page=str(idx),
										min_taken_date = str(starttime),
										max_taken_date = str(t2),									
										text = title.encode('utf-8'),
										extras = 'date_upload, date_taken, owner_name, geo, tags, machine_tags, url_m'
									   )
				idx = idx +1
				self.fapi.testFailure(rsp)
				total_images = rsp.photos[0]['total'];
				null_test = int(total_images);
				
			except:
					null_test = 0
					print sys.exc_info()[0]
					print sys.exc_info()[1]
					print ('Exception encountered while querying title for images\n')
					print type(title),type(title.encode('utf-8'))
			if null_test == 0:
				break
			if null_test >=250*(idx-1):
				bReturn = 1
			else:
				bReturn = 0
				
			tmpdir = os.path.join(gconfig.metadatadir,'querybytitle')
			if not os.path.exists(tmpdir):
				os.makedirs(tmpdir)
			metadata = os.path.join(tmpdir,'%s_%d.xml' % (eventid,idx-1))
			
			data =  parseString(rsp.xml)
			if not os.path.exists(metadata):
				f = open(metadata,'w')		   
				f.write(data.toprettyxml(encoding='UTF-8'))
				f.close() 
			q = data.getElementsByTagName('photo')
			for p in q:
				url = p.getAttribute('url_m')
				if url.find('.jpg')>0:
					photolist.append(url)
		return photolist
	
	def searchbygeo(self,lat,lng,time,eventid):
		photolist = []
		photolist = []
		t1 = time
		t2 = t1 + datetime.timedelta(days = 3)
		starttime = t1 + datetime.timedelta(hours = - (t1.hour))

		bReturn = 1
		idx = 1
		while (bReturn ==1):
			try:			
				rsp = self.fapi.photos_search(api_key=self.api_key,
										ispublic="1",
										media="photos",
										per_page="250", 
										page=str(idx),
										min_taken_date = str(starttime),
										max_taken_date = str(t2),									
										lat  = str(lat),
										lon = str(lng),
										radius = str('0.7'),
										accuracy = '12',
										extras = 'date_upload, date_taken, owner_name, geo, tags, machine_tags, url_m'
									   )
				idx = idx +1
				self.fapi.testFailure(rsp)
				total_images = rsp.photos[0]['total'];
				null_test = int(total_images);
				
			except:
					null_test = 0
					print sys.exc_info()[0]
					print sys.exc_info()[1]
					print ('Exception encountered while querying for images\n')
			if null_test == 0:
				break
			if null_test >=250*(idx-1):
				bReturn = 1
			else:
				bReturn = 0
			tmpdir = os.path.join(gconfig.metadatadir,'querybygeo')
			if not os.path.exists(tmpdir):
				os.makedirs(tmpdir)
			metadata = os.path.join(tmpdir,'%s_%d.xml' % (eventid,idx-1))
			data =  parseString(rsp.xml)
			if not os.path.exists(metadata):
				f = open(metadata,'w')		   
				f.write(data.toprettyxml(encoding='UTF-8'))
				f.close() 
			q = data.getElementsByTagName('photo')
			for p in q:
				url = p.getAttribute('url_m')
				if url.find('.jpg')>0:
					photolist.append(url)
		return photolist
	
	def searchbygeoRadius(self,lat,lng,r,stime,etime, eventid):
		photolist = []
		bReturn = 1
		idx = 1
		while (bReturn ==1):
			try:			
				rsp = self.fapi.photos_search(api_key=self.api_key,
										ispublic="1",
										media="photos",
										per_page="250", 
										page=str(idx),
										min_taken_date = str(stime),
										max_taken_date = str(etime),									
										lat  = str(lat),
										lon = str(lng),
										radius = str(r),
										accuracy = '12',
										extras = 'date_upload, date_taken, owner_name, geo, tags, machine_tags, url_m'
									   )
				idx = idx +1
				self.fapi.testFailure(rsp)
				total_images = rsp.photos[0]['total'];
				null_test = int(total_images);
				
			except:
					null_test = 0
					print sys.exc_info()[0]
					print sys.exc_info()[1]
					print ('Exception encountered while querying for images\n')
			if null_test == 0:
				break
			if null_test >=250*(idx-1):
				bReturn = 1
			else:
				bReturn = 0
			tmpdir = os.path.join(gconfig.metadatadir,'querybygeo')
			if not os.path.exists(tmpdir):
				os.makedirs(tmpdir)
			metadata = os.path.join(tmpdir,'%s_%d.xml' % (eventid,idx-1))
			data =  parseString(rsp.xml)
			if not os.path.exists(metadata):
				f = open(metadata,'w')		   
				f.write(data.toprettyxml(encoding='UTF-8'))
				f.close() 
			q = data.getElementsByTagName('photo')
			for p in q:
				url = p.getAttribute('url_m')
				if url.find('.jpg')>0:
					photolist.append(url)
		return photolist
	
	def outputlist(self,list,id,fname):
		fw = open(fname,'w')
		for url in list:
			fname = url.split('/')[-1]
			fw.write('%s\%s\n' % (id,fname))
		fw.close()

	def geturlbyid(self,id,list):
		photos = {}
		results = []
		for p in list:
			t = p.split('/')[-1]
			t = t.replace('.jpg','')
			photos[t] = p
			
		for idx in id:
			if idx in photos:
				results.append(photos[idx])
		return results
	
	def OutputList(self,listname,lst):
		str = ''
		str += '\n<table align="center"  border="1" cellspacing="1" cellpadding="3" width=800><H2>query by %s</H2><tr>' % listname
		N = len(lst)
		num = 0
		for i in range(0,N):
			img_file = lst[i]		
			str += '\n<td align="center" valign=top width=30><IMG SRC="%s" width=160 border=1 /></td>' % img_file
			num = num +1
			if (num % 8)==0:
				   str +=('</tr>')
		str +=('</table>')
		return str
	
	def OutputJson(self,lst):
		N = len(lst)
		tmp = []
		num = 0
		for i in range(0,N):
			img_file = lst[i]
			tmp.append({'photo':img_file})
		mydict = {}
		mydict['photos'] = tmp
		mydict['number'] = str(len(tmp))
		return mydict
	
	def OutputHtml(self,id,idlist,titlelist,geolist,refinelist):
		file = open(gconfig.outputdir + '/' + '%s.html' % id,'w')
		head='<html><head><title> Media illustration </title></head>'
		file.write('%s\n' % head)
		head='<body BGCOLOR="#FFFFFF"><center><H1>enriching for Event %s</H1><HR HSIZE="50%%"/>' % id
		file.write('%s\n'% head)
		file.write(self.OutputList("machine tag",idlist) )
		file.write(self.OutputList("Geo tag",geolist) )
		file.write(self.OutputList("title + pruning + refine",refinelist) )
		file.close()

	def OutputXML(self,id,idlist,titlelist,geolist,refinelist):
		fname = gconfig.outputdir + '/' + '%s.xml' % id
		setid = set(idlist)
		setgeo = set(geolist) - setid
		settitle = set(titlelist) - setid
		setrefinelist = set(refinelist) - setid
		sets = [setid,setgeo,settitle,setrefinelist]
		tmpinfo = ["query by ID","query by Geo - ID", "query by Title - ID"," Pruning and Refine"]
		doc = Document()
		query = doc.createElement("query")
		query.setAttribute("id",id)
		doc.appendChild(query)
		results = doc.createElement("PhotoSets")
		for tmpset,info in zip(sets,tmpinfo):
			photoset = doc.createElement("photoset")
			photoset.setAttribute('query',info)
			photoset.setAttribute('photoNum',str(len(tmpset)))
			for photo in tmpset:
				ph = doc.createElement("photo")
				ph.setAttribute('url', photo)
				photoset.appendChild(ph)
			results.appendChild(photoset)
		query.appendChild(results)
		f = open(fname, "w")
		f.write(doc.toprettyxml(encoding='UTF-8'))
		f.close()