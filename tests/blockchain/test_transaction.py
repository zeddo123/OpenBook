import sys
sys.path.append('../../')

import unittest
from modules.blockchain.transaction import Transaction
from modules.blockchain.book import Book
from fastecdsa.keys import import_key


class TestTransaction(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		# getting the private and public keys for the test
		cls.private_key, cls.public_key = import_key('tests/blockchain/test_files/default_keyprv.pem')

	def setUp(self):
		book_fortest = Book("Le Gène égoïste", "Richard Dawkins", "1976", "Non-fiction")
		self.transaction_1 = Transaction(self.public_key, self.public_key, book_fortest, self.private_key)
		self.transaction_2 = Transaction(self.public_key, self.public_key, book_fortest, self.private_key, 2)

	def test_to_json(self):
		self.assertEqual(self.transaction_1.to_json(), {
			'type': 1, 
			'sender': str(self.public_key), 
			'recipient': 'the-chain', 
			'book': {
				'title': "Le Gène égoïste", 
				'author': "Richard Dawkins", 
				'date': "1976", 
				'genre': "Non-fiction"
			},
			'signature': str(self.transaction_1.signature)
		})
		self.assertEqual(self.transaction_2.to_json(), {
			'type': 2,
			'sender': 'mining',
			'recipient': str(self.public_key),
			'book': None,
			'signature': 'None'
		})

if __name__ == '__main__':
	unittest.main()