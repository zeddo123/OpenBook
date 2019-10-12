class Book:
	"""docstring for Book"""
	def __init__(self, title, author, date, genre):
		self.title = title
		self.author = author
		self.date = date
		self.genre = genre


	def to_json(self):
		json_dict = {
			'title': self.title,
			'author': self.author,
			'date': self.date,
			'genre': self.genre 
		}
		return json_dict

		