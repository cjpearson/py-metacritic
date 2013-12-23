class Critic:
	def __init__(self,name,publication, cnx):
		values = {}
		values['name'] = str(name) #converts from bs navigable string to unicode string
		values['publication'] = str(publication)

		#add to database
		cursor = cnx.cursor()
		query = ("select critic_id from critics where name = %s and publication = %s")

		inDB = False
		self.cid = 0;
		cursor.execute(query,(values['name'],values['publication']))

		for(critic_id,)in cursor:
			inDB = True
			self.cid = critic_id

		if(not inDB):
			#make a new row for this critic
			add_critic = ("INSERT INTO critics"
	      "(name, publication)"
	      "VALUES (%s, %s)")
			critic_data = (values['name'], values['publication'])
			cursor.execute(add_critic,critic_data)
			self.cid = cursor.lastrowid
			cnx.commit()
		cursor.close()