import urllib
import urllib.request
import re
from bs4 import BeautifulSoup
import requests
import time
import Critic
from Review import Review

class Movie:
	
	def __init__(self, url, cnx):
		
		#temporary for testing
		#url = '/movie/bond-23'

		#skip this. metacritic's fault
		if(url == '/movie/who-the-%-is-jackson-pollock'):
			return
		#values that go into database
		values = {}
		values['title'] = ''
		values['url'] = ''
		values['cScore'] = ''
		values['uScore'] = ''
		values['date'] = ''
		
		#get all of those single values then put them in the movie table
		#then find all of the reviews and put them in the reviews table with the movie id
		
		#time to get the stuff from the movie page
		
		#get movie page
		response = requests.get('http://www.metacritic.com' + url, allow_redirects=True)

		if(response.status_code == 400):
			return
		url = re.sub('http:\/\/www.metacritic.com','',response.url) #resets the url to the one that was redirected to

		#convert html to string
		mainPageHtml = response.content
		#make the soup
		mainPageSoup = BeautifulSoup(mainPageHtml)
			
		#save the url
		values['url'] = url
			
		#get the title
		results = mainPageSoup.find_all('span', {'itemprop' : 'name'})
		values['title'] = results[0].string
		values['title'] = str(values['title'].lstrip().rstrip()) #get rid of weird whitespace
		#get the critic score
		results = mainPageSoup.find_all('span',{'itemprop' : 'ratingValue'})
		values['cScore'] = str(results[0].string)
		
		#get the user score
		results = mainPageSoup.find_all('a', {'class' : 'metascore_anchor', 'href' : url + '/user-reviews'})

		#if for some reason it can't find the user score. it happens even though it shouldn't
		if(len(results)>0):
			values['uScore'] = str(results[0].div.string)
			if(values['uScore']=='tbd'):
				values['uScore'] = str('-1')
		else:
			values['uScore'] = str('-1')		

		#get the year
		results = mainPageSoup.find_all('span', {'class' : 'data', 'itemprop' : 'datePublished'})
		date = str(results[0].string.lstrip().rstrip())
		matches = re.match(r'([a-zA-Z]{3})\s(\d+),\s(\d{4})',date)
		if(matches):
			month = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}[matches.group(1)]
			day = matches.group(2)
			year = matches.group(3)
			values['date'] = year + '-' + month + '-' + day
		else:
			values['date'] = None
		#save to the database
		cursor = cnx.cursor()
		query = ("select movie_id from movies where movie_url = %s")

		inDB = False
		mid=0
		cursor.execute(query,(str(values['url']),))
		for(movie_id,)in cursor:
			inDB = True
			id = movie_id
		if(not inDB):
			#make a new row for this critic
			if(values['date'] is not None):
				add_movie = ("INSERT INTO movies"
		      "(title, movie_url, uScore, cScore, release_date)"
		      "VALUES (%s, %s, %s, %s, %s)")
				movie_data = (values['title'], values['url'], values['uScore'], values['cScore'], values['date'])
			else:
				add_movie = ("INSERT INTO movies"
		      "(title, movie_url, uScore, cScore)"
		      "VALUES (%s, %s, %s, %s)")
				movie_data = (values['title'], values['url'], values['uScore'], values['cScore'])
			cursor.execute(add_movie,movie_data)
			mid = cursor.lastrowid
			cnx.commit()
		cursor.close()

		#get the critic reviews
		#get html
		criticPage = openUrl(url);
		criticSoup = BeautifulSoup(criticPage)	
		
		criticReviews = criticSoup.find_all('div',{'class' : 'module reviews_module critic_reviews_module'})
		if(len(criticReviews)>0):
			reviews = criticReviews[0].find_all('div',{'class' : 'review_content'})
		else:
			print('ERROR:' + url)
			reviews = []

		for r in reviews:
			Rev = Review(mid,values['url'],r, cnx)

def openUrl(url):
	try:
		response = urllib.request.urlopen('http://www.metacritic.com' + url + '/critic-reviews')
		return response.read()
	except:
		openUrl(url)