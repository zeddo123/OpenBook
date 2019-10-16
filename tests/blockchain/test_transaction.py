import sys
sys.path.append('../../')

import unittest
from modules.blockchain.transaction import Transaction
from modules.blockchain.book import Book

class TestTransaction(unittest.TestCase):

	def setUp(self):
		book_fortest = Book("Le Gène égoïste", "Richard Dawkins", "1976", "Non-fiction")
		self.transaction_1 = Transaction("not-mining", "not-data-base", book_fortest)
		self.transaction_2 = Transaction("not-mining", "not-data-base", book_fortest, 2)

	def test_to_json(self):
		self.assertEqual(self.transaction_1.to_json(), {
			'type': 1, 
			'sender': "not-mining", 
			'recipient': "data-base", 
			'book': {
				'title': "Le Gène égoïste", 
				'author': "Richard Dawkins", 
				'date': "1976", 
				'genre': "Non-fiction"
			}
		})
		self.assertEqual(self.transaction_2.to_json(), {
			'type': 2,
			'sender': "mining",
			'recipient': "not-data-base",
			'book': None
		})

if __name__ == '__main__':
	unittest.main()
