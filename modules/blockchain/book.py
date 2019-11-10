class Book:
	"""The Book object contains all the information about a book"""
	def __init__(self, title, author, date, genre):
		"""Object constructor
		
		:param title: title of the Book
		:type title: str
		
		:param author: author of the book
		:type author: str
		
		:param data: the date at which the book has been published
		:param date: str
		
		:param genre: the subject/type of the book
		:type genre: str
		
		"""
		self.title = title
		self.author = author
		self.date = date
		self.genre = genre


	def to_json(self):
		"""
		to_json converts the object into a json object

		:var json_dict: contains information about the book
		:type json_dict: dict

		:returns: a dict (json) containing of the information of the book
		:rtype: dict
		"""
		json_dict = {
			'title': self.title,
			'author': self.author,
			'date': self.date,
			'genre': self.genre 
		}
		return json_dict

	def __eq__(self, other):
		return (self.to_json() == other.to_json())

	def __repr__(self):
		return str(self.to_json())

	def __str__(self):
		return str(self.to_json())