from Critic import Critic

class Review:
	
	def __init__(self, movie_id, movie, soup, cnx):
		values = {}
		values['author'] = ''
		values['publication'] = '' 
		values['score'] =''
		values['movie'] = str(movie)
		values['description'] = ''

		#find author
		AuthorDivFetch = soup.find_all('div',{'class' : 'author'})
		if(len(AuthorDivFetch)>0):
			AuthorLinkSet = AuthorDivFetch[0].find_all('a')
			if(len(AuthorLinkSet)>0):
				values['author'] = str(AuthorLinkSet[0].string)
			else:
				values['author'] = str(AuthorDivFetch[0].find('span',{'class' : 'no_link'}).string)
		else:
			values['author'] = ''

		#find publication
		PublicationDiv = soup.find('div',{'class' : 'source'})
		values['publication'] = str(PublicationDiv.a.string)

		#find score
		ScoreDiv = soup.find_all('div', {'class' : 'review_grade has_author'})
		if(len(ScoreDiv)>0):
			ScoreDiv = ScoreDiv[0]
		else:
			ScoreDiv = soup.find_all('div', {'class' : 'review_grade'})[0]
		values['score'] = str(ScoreDiv.div.string)

		#find text
		DescriptionDiv = soup.find('div',{'class' : 'review_body'})
		values['description'] = str(DescriptionDiv.string).encode('unicode-escape').rstrip().lstrip()
		
		if(values['score']=='tbd'):
			values['score'] = '-1'

		#make a critic object from the Author and Publication
		C = Critic(values['author'],values['publication'],cnx)

		values['critic'] = C
		id = C.cid
		#add to database
		cursor = cnx.cursor()
		query = ("select movie_url from reviews where movie_id = %s and critic_id = %s")
		inDB = False
		cursor.execute(query,(movie_id,id))

		for(movie_url,)in cursor:
			inDB = True
		if(not inDB):
			add_review = ("INSERT INTO reviews"
	      "(movie_url, critic_id, score, movie_id, description)"
	      "VALUES (%s, %s, %s, %s, %s)")
			review_data = (values['movie'], id, values['score'], movie_id, values['description'])
			cursor.execute(add_review,review_data)
		cnx.commit()
		cursor.close()