import sys
sys.path.append('../../')

import unittest
from unittest.mock import patch
from modules.blockchain.block import Block
from modules.blockchain.transaction import Transaction
from modules.blockchain.book import Book
from modules.blockchain.cryptog import Cryptog
import ast

class TestBlock(unittest.TestCase):
	
	@classmethod
	def setUpClass(cls):
		# getting the json files necessary for the test
		with open("tests/blockchain/test_files/json_block.json",'r') as f:
			cls.jsons = ast.literal_eval(f.read())

		# getting the private and public keys for the test
		with open("tests/blockchain/test_files/private_key.pem", 'rb') as f:
			cls.private_key = f.read()
		with open("tests/blockchain/test_files/public_key.pem", 'rb') as f:
			cls.public_key = f.read()


	@patch('modules.blockchain.block.Block.date_time_now', return_value='2019-10-16 19:49:28.800945', autospec=True)
	def setUp(self, mock_datetime):
		book_fortest = Book("Le Gène égoïste", "Richard Dawkins", "1976", "Non-fiction")
		trasaction_1_fortest = Transaction(self.public_key, self.public_key, book_fortest, self.private_key)
		trasaction_2_fortest = Transaction(self.public_key, self.public_key, book_fortest, self.private_key, 2)
		
		transactions_fortest = [trasaction_1_fortest, trasaction_2_fortest]
		
		self.block_1 = Block()
		self.block_2 = Block("49f68a5c8493ec2c0bf489821c21fc3b", transactions_fortest, 1, 258463)
		self.block_3 = Block("49f68a5c8493ec2c0bf489821c21fc3b", transactions_fortest, 1)
		self.block_4 = Block("49f68a5c8493ec2c0bf489821c21fc3b", transactions_fortest)
		self.block_5 = Block("49f68a5c8493ec2c0bf489821c21fc3b")
		self.block_6 = Block(transactions = transactions_fortest)
		self.block_7 = Block(index = 1)
		self.block_8 = Block(nonce = 258463)


	def test_to_json(self):
		self.assertEqual(self.block_1.to_json(hash=True), self.jsons[0])
		print(self.block_2.to_json())
		self.assertEqual(self.block_2.to_json(hash=True), self.jsons[1])
		self.assertEqual(self.block_3.to_json(hash=True), self.jsons[2])
		self.assertEqual(self.block_4.to_json(hash=True), self.jsons[3])
		self.assertEqual(self.block_5.to_json(hash=True), self.jsons[4])
		self.assertEqual(self.block_6.to_json(hash=True), self.jsons[5])
		self.assertEqual(self.block_7.to_json(hash=True), self.jsons[6])
		self.assertEqual(self.block_8.to_json(hash=True), self.jsons[7])


	def test_hash_block(self):
		self.assertEqual(self.block_1.hash_block(),
			'02d72389b7366e51a4270cda1060554c9bde10538ae38c65d9b2f00e2a08b1f6')
		self.assertEqual(self.block_2.hash_block(), 
			'edb6736168a09a77730968670742421bfead5704c9efca2589e6f0c8c12846a3')
		self.assertEqual(self.block_3.hash_block(), 
			'0b9e5682b2563081281d2c5c1acd2b7c3640b94e052f87082951ad8e24bb86a0')
		self.assertEqual(self.block_4.hash_block(), 
			'a8ebda44c2c84f6d1ef9cfcfa379287f959199ef1e8c873409bd5382f161a811')
		self.assertEqual(self.block_5.hash_block(), 
			'6bd746967f61871e934983f806bb1a24932b094fa2e2bd6dd05f4bbafdb20346')
		self.assertEqual(self.block_6.hash_block(), 
			'3c5f86f1179c918fc5c28ecf977b471545ae41701fcb539f8ea145f82d4a6171')
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