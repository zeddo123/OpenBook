import sys
sys.path.append('../../')

import unittest
from modules.blockchain.block import Block
from modules.blockchain.transaction import Transaction
from modules.blockchain.book import Book

class TestBlock(unittest.TestCase):

	def setUp(self):
		book_fortest = Book("Le Gène égoïste", "Richard Dawkins", "1976", "Non-fiction")
		trasaction_1_fortest = Transaction("not-mining", "not-data-base", book_fortest)
		trasaction_2_fortest = Transaction("not-mining", "not-data-base", book_fortest, 2)
		transactions_fortest = [trasaction_1_fortest, trasaction_2_fortest]
		self.transactions_result = [{'type': 1, 'sender': "not-mining", 'recipient': "data-base", 'book': {'title': "Le Gène égoïste", 'author': "Richard Dawkins", 'date': "1976", 'genre': "Non-fiction"}}, 
			{'type': 2, 'sender': "mining", 'recipient': "not-data-base", 'book': None}]
		self.block_1 = Block()
		self.block_1.timestamp = '2019-10-16 19:49:28.800945'
		self.block_2 = Block("49f68a5c8493ec2c0bf489821c21fc3b", transactions_fortest, 1, 258463)
		self.block_2.timestamp = '2019-10-16 19:49:28.800945'
		self.block_3 = Block("49f68a5c8493ec2c0bf489821c21fc3b", transactions_fortest, 1)
		self.block_3.timestamp = '2019-10-16 19:49:28.800945'
		self.block_4 = Block("49f68a5c8493ec2c0bf489821c21fc3b", transactions_fortest)
		self.block_4.timestamp = '2019-10-16 19:49:28.800945'
		self.block_5 = Block("49f68a5c8493ec2c0bf489821c21fc3b")
		self.block_5.timestamp = '2019-10-16 19:49:28.800945'
		self.block_6 = Block(transactions = transactions_fortest)
		self.block_6.timestamp = '2019-10-16 19:49:28.800945'
		self.block_7 = Block(index = 1)
		self.block_7.timestamp = '2019-10-16 19:49:28.800945'
		self.block_8 = Block(nonce = 258463)
		self.block_8.timestamp = '2019-10-16 19:49:28.800945'


	def test_to_json(self):
		self.assertEqual(self.block_1.to_json(), {
			'previous_hash': None,
			'index': 0,
			'transactions': [],
			'nonce': 208393,
			'Timestamp': '2019-10-16 19:49:28.800945'
		})
		self.assertEqual(self.block_2.to_json(), {
			'previous_hash': "49f68a5c8493ec2c0bf489821c21fc3b",
			'index': 1,
			'transactions': self.transactions_result,
			'nonce': 258463,
			'Timestamp': '2019-10-16 19:49:28.800945'
		})
		self.assertEqual(self.block_3.to_json(), {
			'previous_hash': "49f68a5c8493ec2c0bf489821c21fc3b",
			'index': 1,
			'transactions': self.transactions_result,
			'nonce': 208393,
			'Timestamp': '2019-10-16 19:49:28.800945'
		})
		self.assertEqual(self.block_4.to_json(), {
			'previous_hash': "49f68a5c8493ec2c0bf489821c21fc3b",
			'index': 0,
			'transactions': self.transactions_result,
			'nonce': 208393,
			'Timestamp': '2019-10-16 19:49:28.800945'
		})
		self.assertEqual(self.block_5.to_json(), {
			'previous_hash': "49f68a5c8493ec2c0bf489821c21fc3b",
			'index': 0,
			'transactions': [],
			'nonce': 208393,
			'Timestamp': '2019-10-16 19:49:28.800945'
		})
		self.assertEqual(self.block_6.to_json(), {
			'previous_hash': None,
			'index': 0,
			'transactions': self.transactions_result,
			'nonce': 208393,
			'Timestamp': '2019-10-16 19:49:28.800945'
		})
		self.assertEqual(self.block_7.to_json(), {
			'previous_hash': None,
			'index': 1,
			'transactions': [],
			'nonce': 208393,
			'Timestamp': '2019-10-16 19:49:28.800945'
		})
		self.assertEqual(self.block_8.to_json(), {
			'previous_hash': None,
			'index': 0,
			'transactions': [],
			'nonce': 258463,
			'Timestamp': '2019-10-16 19:49:28.800945'
		})


	def test_hash_block(self):
		self.assertEqual(self.block_1.hash_block(),
			'02d72389b7366e51a4270cda1060554c9bde10538ae38c65d9b2f00e2a08b1f6')
		self.assertEqual(self.block_2.hash_block(), 
			'4e8efad075e3e6bcf400afe7d9dfbe4d2160adb488210bd4864dd3843f4d308a')
		self.assertEqual(self.block_3.hash_block(), 
			'4a4df2e5a85ff06c5ce73f8330df75628b42a82d8056b554cf6f690fdae52a67')
		self.assertEqual(self.block_4.hash_block(), 
			'468865905e4fc3f8ff28bb0523e1281019042a53cf9249aa6fc10a8273a5a91e')
		self.assertEqual(self.block_5.hash_block(), 
			'6bd746967f61871e934983f806bb1a24932b094fa2e2bd6dd05f4bbafdb20346')
		self.assertEqual(self.block_6.hash_block(), 
			'd4a34e84b9ad5b6373080e51e56a6ea8968ecc146f8c451db1285287ebaba823')
		self.assertEqual(self.block_7.hash_block(), 
			'f5765a40ef87969bcec557812b8392746b5f77203a3ad1d7d639aa4d39724fa7')
		self.assertEqual(self.block_8.hash_block(), 
			'099773753a36cb773cb62f5990b6dd83d8212d07cbb01e10c2aae206cbe2e8f5')

if __name__ == '__main__':
	unittest.main()
