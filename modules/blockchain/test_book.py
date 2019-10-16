import unittest
from book import Book

class TestBook(unittest.TestCase):

	def setUp(self):
		self.book_1 = Book(
			"A short history of nearly everything", 
			"Bill Bryson", 
			"February 4, 2003", 
			"Non-fiction"
		)
		self.book_2 = Book(
			"Le Gène égoïste", 
			"Richard Dawkins", 
			"1976", 
			"Non-fiction"
		)
		self.book_3 = Book(
			"Harry Potter et la Chambre des secrets J. K. Rowling", 
			"J. K. Rowling", 
			"2 juillet 1998", 
			"‎Fantasy‎"
		)
		self.book_4 = Book(
			"The End of Faith", 
			"Sam Harris", 
			"11/08/2004", 
			"Relegious"
		)

	def test_to_json(self):
		self.assertEqual(self.book_1.to_json(), {
			'title': "A short history of nearly everything", 
			'author': "Bill Bryson", 
			'date': "February 4, 2003",
			'genre': "Non-fiction"
		})
		self.assertEqual(self.book_2.to_json(), {
			'title': "Le Gène égoïste", 
			'author': "Richard Dawkins", 
			'date': "1976", 
			'genre': "Non-fiction"
		})
		self.assertEqual(self.book_3.to_json(), {
			'title': "Harry Potter et la Chambre des secrets J. K. Rowling", 
			'author': "J. K. Rowling", 
			'date': "2 juillet 1998", 
			'genre': "‎Fantasy‎"
		})
		self.assertEqual(self.book_4.to_json(), {
			'title': "The End of Faith", 
			'author': "Sam Harris", 
			'date': "11/08/2004", 
			'genre': "Relegious"
		})

if __name__ == '__main__':
	unittest.main()