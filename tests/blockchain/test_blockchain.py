import sys
sys.path.append('../../')

import unittest
from unittest.mock import patch
from modules.blockchain.blockchain import BlockChain
from modules.blockchain.transaction import Transaction
from modules.blockchain.book import Book
from modules.blockchain.block import Block

class TestBlockchain(unittest.TestCase):

	def setup(self):
		book_fortest = Book("Le Gène égoïste", "Richard Dawkins", "1976", "Non-fiction")
		self.transaction_1 = Transaction("Joe", "recap", book_fortest)
		self.transaction_2 = Transaction("mama", "meme", book_fortest, 2)
		self.blockchain_0 = BlockChain()
		self.blockchain_1 = BlockChain()
		self.blockchain_2 = BlockChain()

	def test_to_json(self):
		pass	

	def test_valid_proof(self):
		pass

	def test_proof_of_work(self):
		pass

	#@patch("modules.blockchain.blockchain.BlockChain.verify_transaction", return_value=True, autospec=True)
	def test_create_append_transaction(self):
		book_fortest = Book("Le Gène égoïste", "Richard Dawkins", "1976", "Non-fiction")
		transaction_1 = Transaction("Joe", "recap", book_fortest)
		transaction_2 = Transaction("mama", "meme", book_fortest, 2)
		blockchain_1 = BlockChain()
		blockchain_2 = BlockChain()
		with patch("modules.blockchain.blockchain.BlockChain.verify_transaction", autospec=True) as mocked_verify:
			mocked_verify.return_value = True
			blockchain_1.create_append_transaction(transaction_1)
			mocked_verify.assert_called_with(blockchain_1, transaction_1)
			self.assertEqual(blockchain_1.open_transactions, [transaction_1])

			mocked_verify.return_value = False
			blockchain_2.create_append_transaction(transaction_2)
			mocked_verify.assert_called_with(blockchain_2, transaction_2)
			self.assertEqual(blockchain_2.open_transactions, [])

	@patch('modules.blockchain.block.Block.date_time_now', return_value='2019-10-16 19:49:28.800945', autospec=True)
	def test_mine_block(self, mock_datetime):
		book_fortest = Book("Le Gène égoïste", "Richard Dawkins", "1976", "Non-fiction")
		transaction_1 = Transaction("Joe", "recap", book_fortest)
		transaction_2 = Transaction("mama", "meme", book_fortest, 2)
		block_0 = Block(None,[Transaction(sender=None, recipient='BlockChain', book=None, transaction_type=2)])

		blockchain_1 = BlockChain()
		blockchain_1.open_transactions.append(transaction_1)
		op_trans_1 = blockchain_1.open_transactions
		op_trans_1.append(Transaction(sender=None, recipient="recipient", book=None, transaction_type=2))
		block_1 = Block('ece8c1c5b1d61f6455afb421c3869ab51ef12e4b2f1cfde652602a6e83fdd4ac', op_trans_1, index=1, nonce=208395)

		blockchain_2 = BlockChain()
		blockchain_2.open_transactions.append(transaction_2)
		op_trans_2 = blockchain_2.open_transactions
		op_trans_2.append(Transaction(sender=None, recipient="recipient", book=None, transaction_type=2))
		block_2 = Block('ece8c1c5b1d61f6455afb421c3869ab51ef12e4b2f1cfde652602a6e83fdd4ac', op_trans_2, index=1, nonce=426969)

		with patch("modules.blockchain.blockchain.BlockChain.proof_of_work", autospec=True) as mocked_nonce:
			mocked_nonce.return_value = 208395
			blockchain_1.mine_block('zeddo')
			self.assertEqual(blockchain_1.block_chain, [block_0, block_1])
			self.assertEqual(blockchain_1.open_transactions, [])

			mocked_nonce.return_value = 426969
			blockchain_2.mine_block('maistro')
			self.assertEqual(blockchain_2.block_chain, [block_0, block_2])
			self.assertEqual(blockchain_2.open_transactions, [])


	def test_number_blocks(self):
		pass

if __name__ == '__main__':
	unittest.main()