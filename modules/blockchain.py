from block import *
from transaction import *
from book import *


class BlockChain:
	"""docstring for BlockChain"""
	def __init__(self):
		self.block_chain = []
		genesis_block = Block(None,[Transaction(sender=None, recipient='BlockChain', book=None, transaction_type=2)])
		self.block_chain.append(genesis_block)
		self.open_transactions = []


	def valid_proof(self, last_hash, nonce):
		guess = (str(list(map(str, self.open_transactions))) + str(last_hash) + str(nonce)).encode()

		guess_hash = hashlib.sha256(guess).hexdigest()

		print(guess_hash)

		return guess_hash[0:2] == '42'


	def proof_of_work(self):
		last_block = self.block_chain[-1]
		last_hash = last_block.hash_block()

		nonce = 0
		while not self.valid_proof(last_hash, nonce):
			nonce += 1

		return nonce
	

	def create_append_transaction(self, sender, recipient, book, transaction_type=1):
		new_transaction = Transaction(sender,recipient,book,transaction_type)
		self.open_transactions.append(new_transaction)


	def mine_block(self, recipient):
		last_block = self.block_chain[-1]
		last_hash = last_block.hash_block()

		nonce = self.proof_of_work()

		reward_transaction = Transaction(sender=None, recipient=recipient, book=None, transaction_type=2)
		self.open_transactions.append(reward_transaction)

		new_block = Block(last_hash,self.open_transactions,index=len(self.block_chain),nonce=nonce)

		self.block_chain.append(new_block)

		self.open_transactions = []

	def __str__(self):
		print(f'::{len(self.block_chain)} blocks in the blockchain')
		for block, number in zip(self.block_chain, range(len(self.block_chain))):
			print('number\n',number)
			print('block\n', block)
		return ''

if __name__ == '__main__':
	blockchain = BlockChain()
	print(blockchain)
	blockchain.create_append_transaction('mouha','recipient',Book(title='The Selfish Gene',author='Richard Dawkins', date='19--', genre='Science'))
	blockchain.mine_block('mouha')
	print(blockchain)