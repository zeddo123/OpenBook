import sys

sys.path.append('../../')

import unittest
from unittest.mock import patch
from modules.blockchain.block import Block
from modules.blockchain.transaction import Transaction
from modules.blockchain.book import Book
from fastecdsa.keys import import_key
from fastecdsa.curve import secp256k1
import ast


class TestBlock(unittest.TestCase):
	
	@classmethod
	def setUpClass(cls):
		# getting the json files necessary for the test
		with open("tests/blockchain/test_files/json_block.json",'r') as f:
			cls.jsons = ast.literal_eval(f.read())

		# getting the private and public keys for the test
		cls.private_key, cls.public_key = import_key('tests/blockchain/test_files/default_keyprv.pem', curve=secp256k1)


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
		# TODO: The first test seams to fail, because of a difference in the transactions
		self.assertEqual(self.block_1.to_json(hash=True), self.jsons[0])
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
			'422958ad5960ec69934c640204e0bc9a6f20aeae20cef040a617741d4719d013')
		self.assertEqual(self.block_3.hash_block(), 
			'9a1480c3480b6d88469aec89618a453da6bb31b8ba1cce2d9718638f2aadde47')
		self.assertEqual(self.block_4.hash_block(), 
			'f06c5d99239dead346ad0dfc52aa881353ed6571ce203feece3437eb22904488')
		self.assertEqual(self.block_5.hash_block(), 
			'6bd746967f61871e934983f806bb1a24932b094fa2e2bd6dd05f4bbafdb20346')
		self.assertEqual(self.block_6.hash_block(), 
			'99a085ab962ddc5e3e72dd7efb589a1e30f17d987a94b08f22f797a41dc3d8e8')
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


	@classmethod
	def setUpClass(cls):
		# getting the json files necessary for the test
		with open("tests/blockchain/test_files/json_block.json", 'r') as f:
			cls.jsons = ast.literal_eval(f.read())

		# getting the private and public keys for the test
		cls.private_key, cls.public_key = import_key('tests/blockchain/test_files/default_keyprv.pem')

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
		self.block_6 = Block(transactions=transactions_fortest)
		self.block_7 = Block(index=1)
		self.block_8 = Block(nonce=258463)

	def test_to_json(self):
		self.assertEqual(self.block_1.to_json(hash=True), self.jsons[0])
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
						'422958ad5960ec69934c640204e0bc9a6f20aeae20cef040a617741d4719d013')
		self.assertEqual(self.block_3.hash_block(),
						'9a1480c3480b6d88469aec89618a453da6bb31b8ba1cce2d9718638f2aadde47')
		self.assertEqual(self.block_4.hash_block(),
						'f06c5d99239dead346ad0dfc52aa881353ed6571ce203feece3437eb22904488')
		self.assertEqual(self.block_5.hash_block(),
						'6bd746967f61871e934983f806bb1a24932b094fa2e2bd6dd05f4bbafdb20346')
		self.assertEqual(self.block_6.hash_block(),
						'99a085ab962ddc5e3e72dd7efb589a1e30f17d987a94b08f22f797a41dc3d8e8')
		self.assertEqual(self.block_7.hash_block(),
						'f5765a40ef87969bcec557812b8392746b5f77203a3ad1d7d639aa4d39724fa7')
		self.assertEqual(self.block_8.hash_block(),
						'099773753a36cb773cb62f5990b6dd83d8212d07cbb01e10c2aae206cbe2e8f5')

	def test_json_to_block(self):
		block_3 = Block("49f68a5c8493ec2c0bf489821c21fc3b")

		b_json = block_3.to_json()
		new_block = Block.json_to_block(b_json)

		self.assertEqual(new_block, block_3)

		# verify if the transactions are of a list type
		self.assertEqual(type(new_block.transactions), list)



if __name__ == '__main__':
    unittest.main()
