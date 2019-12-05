import sys
sys.path.append('../../')


from contextlib import contextmanager
import unittest
from unittest.mock import patch
from modules.blockchain.blockchain import BlockChain
from modules.blockchain.transaction import Transaction
from modules.blockchain.book import Book
from modules.blockchain.block import Block


class TestBlockchain(unittest.TestCase):

	@patch('modules.blockchain.block.Block.hash_block', return_value='96b1255447ec94f9df2e7ad8d8e7d8106bd9b26ebba7fd97d0f3fb423afc961e', autospec=True)
	@patch('modules.blockchain.block.Block.date_time_now', return_value='2019-10-16 19:49:28.800945', autospec=True)
	def setUp(self, mock_datetime, mock_hash_block):
		book_fortest = Book("Le Gène égoïste", "Richard Dawkins", "1976", "Non-fiction")
		self.transaction_1 = Transaction("Joe", "recap", book_fortest)
		self.transaction_2 = Transaction("mama", "meme", book_fortest, 2)
		self.block_0 = Block(None,[Transaction(sender=None, recipient='BlockChain', book=None, transaction_type=2)])
		self.block_1 = Block('96b1255447ec94f9df2e7ad8d8e7d8106bd9b26ebba7fd97d0f3fb423afc961e', [], index=1, nonce=208395)
		self.block_2 = Block('96b1255447ec94f9df2e7ad8d8e7d8106bd9b26ebba7fd97d0f3fb423afc961e', [], index=1, nonce=426969)
		self.blockchain_0 = BlockChain()
		self.blockchain_1 = BlockChain()
		self.blockchain_2 = BlockChain()


	def test_to_json(self):
		self.assertEqual(self.blockchain_0.to_json(), 
			{0: {
				'previous_hash': None, 
				'index': 0, 
				'transactions': [{'type': 2, 'sender': 'mining', 'recipient': 'BlockChain', 'book': None}], 
				'nonce': 208393, 
				'Timestamp': '2019-10-16 19:49:28.800945',
				'hash': self.blockchain_0.block_chain[0].hash
				}
			})

		self.blockchain_0.block_chain.append(self.block_0)
		self.assertEqual(self.blockchain_0.to_json(),
			{
			0: {
				'previous_hash': None, 
				'index': 0, 
				'transactions': [{'type': 2, 'sender': 'mining', 'recipient': 'BlockChain', 'book': None}], 
				'nonce': 208393, 
				'Timestamp': '2019-10-16 19:49:28.800945',
				'hash': self.blockchain_0.block_chain[0].hash
				},
			1: {
				'previous_hash': None, 
				'index': 0, 
				'transactions': [{'type': 2, 'sender': 'mining', 'recipient': 'BlockChain', 'book': None}], 
				'nonce': 208393, 
				'Timestamp': '2019-10-16 19:49:28.800945',
				'hash': self.blockchain_0.block_chain[1].hash
				}
			})

		self.blockchain_0.block_chain.extend([self.block_1, self.block_2])
		self.assertEqual(self.blockchain_0.to_json(),
			{
			0: {
				'previous_hash': None, 
				'index': 0, 
				'transactions': [{'type': 2, 'sender': 'mining', 'recipient': 'BlockChain', 'book': None}], 
				'nonce': 208393, 
				'Timestamp': '2019-10-16 19:49:28.800945',
				'hash': self.blockchain_0.block_chain[0].hash
				}, 
			1: {
				'previous_hash': None, 
				'index': 0, 
				'transactions': [{'type': 2, 'sender': 'mining', 'recipient': 'BlockChain', 'book': None}], 
				'nonce': 208393, 
				'Timestamp': '2019-10-16 19:49:28.800945',
				'hash': self.blockchain_0.block_chain[1].hash
				}, 
			2: {
				'previous_hash': '96b1255447ec94f9df2e7ad8d8e7d8106bd9b26ebba7fd97d0f3fb423afc961e', 
				'index': 1, 
				'transactions': [], 
				'nonce': 208395, 
				'Timestamp': '2019-10-16 19:49:28.800945',
				'hash': self.blockchain_0.block_chain[2].hash
				}, 
			3: {
				'previous_hash': '96b1255447ec94f9df2e7ad8d8e7d8106bd9b26ebba7fd97d0f3fb423afc961e', 
				'index': 1, 
				'transactions': [], 
				'nonce': 426969, 
				'Timestamp': '2019-10-16 19:49:28.800945',
				'hash': self.blockchain_0.block_chain[3].hash
				}
			})


	def test_valid_proof(self):
		last_hash = '96b1255447ec94f9df2e7ad8d8e7d8106bd9b26ebba7fd97d0f3fb423afc961e'
		self.blockchain_1.open_transactions.append(self.transaction_1)
		nonce = 0
		self.assertEqual(self.blockchain_1.valid_proof(last_hash, nonce), False)
		nonce = 12
		self.assertEqual(self.blockchain_1.valid_proof(last_hash, nonce), False)
		nonce = 34
		self.assertEqual(self.blockchain_1.valid_proof(last_hash, nonce), False)
		nonce = 202
		self.assertEqual(self.blockchain_1.valid_proof(last_hash, nonce), True)

		self.blockchain_2.open_transactions.append(self.transaction_2)
		nonce = 0
		self.assertEqual(self.blockchain_2.valid_proof(last_hash, nonce), False)
		nonce = 485
		self.assertEqual(self.blockchain_2.valid_proof(last_hash, nonce), False)
		nonce = 202
		self.assertEqual(self.blockchain_2.valid_proof(last_hash, nonce), False)
		nonce = 34
		self.assertEqual(self.blockchain_2.valid_proof(last_hash, nonce), True)


	def test_proof_of_work(self):
		with patch("modules.blockchain.blockchain.BlockChain.valid_proof", autospec=True) as mocked_valid_proof:
			mocked_valid_proof = True
			self.assertEqual(self.blockchain_0.proof_of_work(), 0)


	def test_create_append_transaction(self):
		with patch("modules.blockchain.blockchain.BlockChain.verify_transaction", autospec=True) as mocked_verify:
			mocked_verify.return_value = True
			self.blockchain_1.create_append_transaction(self.transaction_1)
			mocked_verify.assert_called_with(self.blockchain_1, self.transaction_1)
			self.assertEqual(self.blockchain_1.open_transactions, [self.transaction_1])

			mocked_verify.return_value = False
			self.blockchain_2.create_append_transaction(self.transaction_2)
			mocked_verify.assert_called_with(self.blockchain_2, self.transaction_2)
			self.assertEqual(self.blockchain_2.open_transactions, [])


	@patch('modules.blockchain.block.Block.hash_block', return_value='96b1255447ec94f9df2e7ad8d8e7d8106bd9b26ebba7fd97d0f3fb423afc961e', autospec=True)
	@patch('modules.blockchain.block.Block.date_time_now', return_value='2019-10-16 19:49:28.800945', autospec=True)
	def test_mine_block(self, mock_datetime, mock_hash_block):

		self.blockchain_1.open_transactions.append(self.transaction_1)
		op_trans_1 = list(self.blockchain_1.open_transactions)
		op_trans_1.append(Transaction(sender=None, recipient='zeddo', book=None, transaction_type=2))
		self.block_1.transactions = list(op_trans_1)

		self.blockchain_2.open_transactions.append(self.transaction_2)
		op_trans_2 = list(self.blockchain_2.open_transactions)
		op_trans_2.append(Transaction(sender=None, recipient='maistro', book=None, transaction_type=2))
		self.block_2.transactions = list(op_trans_2)

		with patch("modules.blockchain.blockchain.BlockChain.proof_of_work", autospec=True) as mocked_nonce:
			mocked_nonce.return_value = 208395
			self.blockchain_1.mine_block('zeddo')
			# TODO: Fix the assert Equal
			# Issue '#48' on taiga
			self.assertEqual(self.blockchain_1.block_chain, [self.block_0, self.block_1])
			self.assertEqual(self.blockchain_1.open_transactions, [])

			mocked_nonce.return_value = 426969
			self.blockchain_2.mine_block('maistro')
			self.assertEqual(self.blockchain_2.block_chain, [self.block_0, self.block_2])
			self.assertEqual(self.blockchain_2.open_transactions, [])


	def test_number_blocks(self):
		self.assertEqual(self.blockchain_0.number_blocks(), 1)
		self.blockchain_0.block_chain.extend([self.block_0, self.block_1, self.block_2])
		self.assertEqual(self.blockchain_0.number_blocks(), 4)

	def test_verify_transaction(self):
		pass

	def test_verify_blockchain(self):
		
		block_0 = Block(None, [], index=1, nonce=208395)
		block_1 = Block(block_0.hash, [], index=2)
		
		self.blockchain_0.block_chain = [block_0, block_1]
		self.blockchain_0.debug = False

		# Test for Timestamps irregularities
		
		# timestamps of block_0 == timestamps of block_1
		block_1.timestamp = block_0.timestamp
		self.assertEqual(BlockChain.verify_blockchain(self.blockchain_0), False)

		# timestamps of block_0 < timestamps of block_1
		block_1.timestamp = block_1.date_time_now()
		block_1.hash = block_1.hash_block()
		self.assertEqual(BlockChain.verify_blockchain(self.blockchain_0), True)

		#Test for hash and previous hash
		
		# block_0.hash == block_1.previous_hash
		self.assertEqual(BlockChain.verify_blockchain(self.blockchain_0), True)
		
		# block_0.hash != block_1.previous_hash
		block_1.previous_hash = "random SHA_256 hash"
		self.assertEqual(BlockChain.verify_blockchain(self.blockchain_0), False)
		block_1.previous_hash = block_0.hash

		# Test for hash irregularities
		
		# hash of block == calculated one
		self.assertEqual(BlockChain.verify_blockchain(self.blockchain_0), True)
		
		# hash of block different for the calculated one 
		block_1.transactions = [Transaction(sender=None, recipient='maistro', book=None, transaction_type=2)]
		self.assertEqual(BlockChain.verify_blockchain(self.blockchain_0), False)

	def test_fork_chain(self):
		chain = BlockChain()
		chain.block_chain = [self.block_0, self.block_1, self.block_2]
		
		# Testing the equality of a fork (big fork)
		copy_chain = chain.fork_chain()
		self.assertEqual(chain == copy_chain, True)

		# Testing the equality of a fork if the fork is partial
		copy_chain = chain.fork_chain(1)

		with blockchain_restore(chain, [self.block_1, self.block_2], attr='block_chain') as tmp_chain:
			self.assertEqual(tmp_chain == copy_chain, True)

	def test_json_to_blockchain(self):
		block_0 = Block(None, [], index=1, nonce=208395)
		block_1 = Block(block_0.hash, [], index=2)
		
		self.blockchain_0.block_chain = [block_0, block_1]
		self.blockchain_0.debug = False

		bc_json = self.blockchain_0.to_json()
		new_bc = BlockChain.json_to_blockchain(bc_json)

		self.assertEqual(new_bc,self.blockchain_0)

@contextmanager
def blockchain_restore(chain, value, attr):
	try:
		old_attr = getattr(chain,attr)
		setattr(chain, attr, value)
		yield chain
	finally:
		setattr(chain, attr, old_attr)

if __name__ == '__main__':
	unittest.main()