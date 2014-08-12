

from safeData import safeData
import re
import datetime
from xml.dom.minidom import parseString
import socket
import simplejson
import urllib

socket.setdefaulttimeout(90)

class eventinfo():
	def __init__(self,url):
		self.geteventinfo(url)
		
	def getOriginalURL(self,url):
		query = '''prefix  lode: <http://linkedevents.org/ontology/>
					prefix owl: <http://www.w3.org/2002/07/owl#>
					SELECT ?event
					WHERE {
					<eventURI> owl:sameAs ?event
					}
					'''
		query = query.replace('eventURI',url)
		searchbase = 'http://eventmedia.eurecom.fr/sparql'
		params = urllib.urlencode({"format": "application/sparql-results+json", "query": query})
		f = urllib.urlopen(searchbase + '?' + params)
		try:
			results = simplejson.load(f)
			results = results['results']['bindings']
			event = results[0]
			return event['event']['value']
		except:
			return url
		
	def getEventMediaURL(self,url):
		query = '''prefix  lode: <http://linkedevents.org/ontology/>
					prefix owl: <http://www.w3.org/2002/07/owl#>
					SELECT ?event
					WHERE {
					?event owl:sameAs <eventURI>
					}
					'''
		query = query.replace('eventURI',url)
		searchbase = 'http://eventmedia.eurecom.fr/sparql'
		params = urllib.urlencode({"format": "application/sparql-results+json", "query": query})
		f = urllib.urlopen(searchbase + '?' + params)
		try:
			results = simplejson.load(f)
			results = results['results']['bindings']
			event = results[0]
			return event['event']['value']
		except:
			return url
		
	def geteventinfo(self,url):
		if url.find('data.linkedevents.org') < 0: # not in event media
			self.url = self.getEventMediaURL(url)
			self.originalurl = url
		else:
			self.url = url
			self.originalurl = self.getOriginalURL(url)
			
		self.id = self.url.split('/')[-1]
		
		query = "prefix  lode: <http://linkedevents.org/ontology/> \n\
				prefix	dc: <http://purl.org/dc/elements/1.1/> \n\
				prefix	ma: <http://www.w3.org/ns/ma-ont#> \n\
				prefix wgs84: <http://www.w3.org/2003/01/geo/wgs84_pos#> \n\
				prefix  time: <http://www.w3.org/2006/time#> \n\
				SELECT ?event ?eventTitle ?venueName ?lat ?long ?startDate ?endDate \n\
				WHERE { \n\
				 ?event dc:title ?eventTitle. \n\
				 ?event lode:atPlace ?venue. \n\
				 ?venue rdfs:label ?venueName. \n\
				 ?event lode:inSpace ?location. \n\
				 ?location wgs84:lat ?lat. \n\
				 ?location wgs84:long ?long. \n\
				 ?event lode:atTime ?time. \n\
				 OPTIONAL { \n\
				   { ?time time:inXSDDateTime ?startDate. } \n\
				   UNION \n\
				   { ?time time:hasBeginning ?x. \n\
					 ?x time:inXSDDateTime ?startDate. \n\
					 ?time time:hasEnd ?y. \n\
					 ?y time:inXSDDateTime ?endDate. \n\
				   } \n\
				 } \n\
				 FILTER (?event = <eventURI>). \n\
				}  \n\
				"
		query = query.replace('eventURI',self.url)

		searchbase = 'http://eventmedia.eurecom.fr/sparql'
		params = urllib.urlencode({"format": "application/sparql-results+json", "query": query})
		f = urllib.urlopen(searchbase + '?' + params)
		try:
		    results = simplejson.load(f)
		except:
		    self.succ = -1
		    return []
		try:
		    results = results['results']['bindings']
		except:
			self.succ = 0
			return []
		self.succ = 1
		try:
			event = results[0]
		except:
			print query
			raise
		
		self.title = event['eventTitle']['value']
		t = event['startDate']['value'].split('+')	
		self.stime = t[0]

		self.venue = event['venueName']['value']
		
		t = event['lat']['value']
		self.lat = float(t)
		t = event['long']['value']
		self.lng = float(t)