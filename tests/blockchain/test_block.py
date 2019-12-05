import sys
sys.path.append('../../')

import unittest
from unittest.mock import patch
from modules.blockchain.block import Block
from modules.blockchain.transaction import Transaction
from modules.blockchain.book import Book


class TestBlock(unittest.TestCase):

	@patch('modules.blockchain.block.Block.date_time_now', return_value='2019-10-16 19:49:28.800945', autospec=True)
	def setUp(self, mock_datetime):
		book_fortest = Book("Le Gène égoïste", "Richard Dawkins", "1976", "Non-fiction")
		trasaction_1_fortest = Transaction("not-mining", "not-data-base", book_fortest)
		trasaction_2_fortest = Transaction("not-mining", "not-data-base", book_fortest, 2)
		
		transactions_fortest = [trasaction_1_fortest, trasaction_2_fortest]
		self.transactions_result = [
			{'type': 1, 'sender': "not-mining", 'recipient': "the-chain", 'book': {'title': "Le Gène égoïste", 'author': "Richard Dawkins", 'date': "1976", 'genre': "Non-fiction"}}, 
			{'type': 2, 'sender': "mining", 'recipient': "not-data-base", 'book': None}
		]
		
		self.block_1 = Block()
		self.block_2 = Block("49f68a5c8493ec2c0bf489821c21fc3b", transactions_fortest, 1, 258463)
		self.block_3 = Block("49f68a5c8493ec2c0bf489821c21fc3b", transactions_fortest, 1)
		self.block_4 = Block("49f68a5c8493ec2c0bf489821c21fc3b", transactions_fortest)
		self.block_5 = Block("49f68a5c8493ec2c0bf489821c21fc3b")
		self.block_6 = Block(transactions = transactions_fortest)
		self.block_7 = Block(index = 1)
		self.block_8 = Block(nonce = 258463)


	def test_to_json(self):
		# TODO: The first test seams to fail, because of a difference in the transactions
		self.assertEqual(self.block_1.to_json(hash=True), {
			'previous_hash': None,
			'index': 0,
			'transactions': [],
			'nonce': 208393,
			'Timestamp': '2019-10-16 19:49:28.800945'
		})
		self.assertEqual(self.block_2.to_json(hash=True), {
			'previous_hash': "49f68a5c8493ec2c0bf489821c21fc3b",
			'index': 1,
			'transactions': self.transactions_result,
			'nonce': 258463,
			'Timestamp': '2019-10-16 19:49:28.800945'
		})
		self.assertEqual(self.block_3.to_json(hash=True), {
			'previous_hash': "49f68a5c8493ec2c0bf489821c21fc3b",
			'index': 1,
			'transactions': self.transactions_result,
			'nonce': 208393,
			'Timestamp': '2019-10-16 19:49:28.800945'
		})
		self.assertEqual(self.block_4.to_json(hash=True), {
			'previous_hash': "49f68a5c8493ec2c0bf489821c21fc3b",
			'index': 0,
			'transactions': self.transactions_result,
			'nonce': 208393,
			'Timestamp': '2019-10-16 19:49:28.800945'
		})
		self.assertEqual(self.block_5.to_json(hash=True), {
			'previous_hash': "49f68a5c8493ec2c0bf489821c21fc3b",
			'index': 0,
			'transactions': [],
			'nonce': 208393,
			'Timestamp': '2019-10-16 19:49:28.800945'
		})
		self.assertEqual(self.block_6.to_json(hash=True), {
			'previous_hash': None,
			'index': 0,
			'transactions': self.transactions_result,
			'nonce': 208393,
			'Timestamp': '2019-10-16 19:49:28.800945'
		})
		self.assertEqual(self.block_7.to_json(hash=True), {
			'previous_hash': None,
			'index': 1,
			'transactions': [],
			'nonce': 208393,
			'Timestamp': '2019-10-16 19:49:28.800945'
		})
		self.assertEqual(self.block_8.to_json(hash=True), {
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
			'18efb5509ef19a22b5079d1b0548ae75494a823721ec33e1b668f2c2db2f0bdb')
		self.assertEqual(self.block_3.hash_block(), 
			'1e05e8c9eda3344df4b34b67e7085caffc5615c12f2d7c4e7c854fabd5842ab8')
		self.assertEqual(self.block_4.hash_block(), 
			'1f74d604c09fb7fff4696c5769f1e7c28f73de78a165f2bb149312f5edf5811f')
		self.assertEqual(self.block_5.hash_block(), 
			'6bd746967f61871e934983f806bb1a24932b094fa2e2bd6dd05f4bbafdb20346')
		self.assertEqual(self.block_6.hash_block(), 
			'6cdd76f3d278f3255eafc4e3830e99118b3e0ccefeba8bef73cebc9be47519a7')
		self.assertEqual(self.block_7.hash_block(), 
			'f5765a40ef87969bcec557812b8392746b5f77203a3ad1d7d639aa4d39724fa7')
		self.assertEqual(self.block_8.hash_block(), 
			'099773753a36cb773cb62f5990b6dd83d8212d07cbb01e10c2aae206cbe2e8f5')

	def test_json_to_block(self):
		block_3 = Block("49f68a5c8493ec2c0bf489821c21fc3b")

		b_json = block_3.to_json()
		new_block = Block.json_to_block(b_json)
		
		self.assertEqual(new_block,block_3)

		#verify if the transactions are of a list type
		self.assertEqual(type(new_block.transactions),list)


if __name__ == '__main__':
	unittest.main()