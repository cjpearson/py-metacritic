import urllib
import re
from bs4 import BeautifulSoup
import requests
import mysql.connector
from Movie import Movie
import time
from configparser import ConfigParser


def openPage(url):
	#get html
	completeURL = 'http://www.metacritic.com' + url
	#response = requests.get(completeURL, allow_redirects=False)
	response = urllib.request.urlopen(completeURL)
	#convert html to string
	html = response.read()
	#make the soup
	soup = BeautifulSoup(html)
	#find the next button
	nextUrlFetch = soup.find_all("link",rel="next")
	#if it finds the next link
	if(nextUrlFetch):
		nextUrl = nextUrlFetch[0]['href']
		finished = False
	else:
		#if there is no previous link either the page didn't load or something. try again
		if(len(soup.find_all('link', rel = 'prev'))<1):
			print('something may be wrong. trying to open link again')
			openPage(url)
			finished = False
		else:
			finished = True

	#get the links to each movie
	movieArea = soup.find('div', {'class' : 'body_wrap'})
	movies = movieArea.find_all('div' , {'class' : 'product_wrap'})

	links = []
	for m in movies:
		linkDiv = m.find('div')
		links.append(linkDiv.a['href'])
	
	#go to each link and fetch all of the reviews
	for url in links:
		print(url)
		M = Movie(url,cnx)

	#if there is a next link
	if(nextUrlFetch):
		openPage(nextUrl)
	#if there is no next link
	else:
		if(finished):
			print('finished')
			return

#read database information from db.ini file. Thanks wells oliver
parser = ConfigParser()
parser.read('db.ini')
user = parser.get('db', 'user')
password = parser.get('db', 'password')
db = parser.get('db', 'db')
                
args = {'user': user, 'passwd': password, 'db': db}
if parser.has_option('db', 'host'):
	args['host'] = parser.get('db', 'host')

print(args)
cnx = mysql.connector.connect(user=args['user'], password=args['passwd'], database=args['db'])
openPage('/browse/movies/score/metascore/all?sort=desc&view=condensed&page=1')
cnx.close()
