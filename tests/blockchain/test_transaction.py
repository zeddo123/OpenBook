import sys
sys.path.append('../../')

import unittest
from modules.blockchain.transaction import Transaction
from modules.blockchain.book import Book
from modules.blockchain.cryptog import Cryptog


class TestTransaction(unittest.TestCase):

	def setUp(self):
		self.crp_1 = Cryptog()
		self.crp_2 = Cryptog()
		self.crp_1.generate_keys()
		self.crp_2.generate_keys()

		book_fortest = Book("Le Gène égoïste", "Richard Dawkins", "1976", "Non-fiction")
		self.transaction_1 = Transaction(self.crp_1.public_key, self.crp_2.public_key, book_fortest, self.crp_1.private_key)
		self.transaction_2 = Transaction(self.crp_2.public_key, self.crp_1.public_key, book_fortest, self.crp_2.private_key, 2)

	def test_to_json(self):
		self.assertEqual(self.transaction_1.to_json(), {
			'type': 1, 
			'sender': self.crp_1.public_key, 
			'recipient': 'the-chain', 
			'book': {
				'title': "Le Gène égoïste", 
				'author': "Richard Dawkins", 
				'date': "1976", 
				'genre': "Non-fiction"
			},
			'signature': self.transaction_1.signature
		})
		self.assertEqual(self.transaction_2.to_json(), {
			'type': 2,
			'sender': 'mining',
			'recipient': self.crp_1.public_key,
			'book': None,
			'signature': self.transaction_2.signature
		})

if __name__ == '__main__':
	unittest.main()