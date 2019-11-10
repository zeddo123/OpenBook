from modules.blockchain.block import *
from modules.blockchain.transaction import *
from modules.blockchain.book import *


class BlockChain:
	"""BlockChain Object to be added to the chain

	:Attributes:

		:attr block_chain: All the blocks in the chain
		:type block_chain: list
		
		:attr open_transaction: All the transactions to be added
		:type open_transaction: list

	:Methods:
	
		:meth __init__: Constructor of the class
		
		:meth to_json: Create a json file of the block-chain
		
		:meth valid_proof: Verify the hash guess
		
		:meth proof_of_work: Calculate the hash of the block and return nonce
		
		:meth create_append_transaction: Create and append a transaction to the open transaction list
		
		:meth mine_block: mine the new block + add the reward transaction
		
		:meth number_blocks: gives number of block in the chain
		
		:meth __str__: magic method, prints the chain and its blocks

	"""

	def __init__(self):
		"""Constructor of the class"""

		self.block_chain = []

		# Create the genesis block (the first block in the chain)
		genesis_block = Block(None,[Transaction(sender=None, recipient='BlockChain', book=None, transaction_type=2)])
		
		self.block_chain.append(genesis_block)
		self.open_transactions = []


	def valid_proof(self, last_hash, nonce):
		"""Verify the hash guess
		
		:param last_hash: the hash of the previous block in the chain
		:type last_hash: str
		
		:param nonce: nonce guess of the hash
		:type nonce: int
		
		:returns: True or False guess_hash
		:rtype: bool
		
		"""

		guess = (str(list(map(str, self.open_transactions))) + str(last_hash) + str(nonce)).encode()

		guess_hash = hashlib.sha256(guess).hexdigest()

		print(guess_hash)

		return guess_hash[0:2] == '42' # 42 is the difficulty to find the hash


	def proof_of_work(self):
		"""Search for the right hash by adjusting the `nonce` value
		
		:var nonce: field whose value is adjusted by miners so that the hash of
			the block will be the current target (for now it's 42 as the first two chars) of the network
		:type nonce: int
		
		:returns: nonce of the hash
		:rtype: int
		"""

		last_block = self.block_chain[-1]
		last_hash = last_block.hash_block()

		nonce = 0
		while not self.valid_proof(last_hash, nonce):
			nonce += 1

		return nonce
	
	# TODO: change the name of this method
	def create_append_transaction(self, new_transaction):
		"""This method create a transaction and append it to the Open transaction attr
		
		:param new_transaction: new transaction
		:type new_transaction: Transaction object -> *`modules.blockchain.transaction`*
		
		:returns: None
		"""
		if self.verify_transaction(new_transaction):
			self.open_transactions.append(new_transaction)

	def verify_transaction(self, new_transaction): #TODO: complete this method
		pass


	def mine_block(self, recipient):
		"""This method mine the new block with the opentransaction list

		:param recipient: Miner's ID - who is being rewarded for mining the block 
		:type recipient: str

		:returns: None
		"""
		last_block = self.block_chain[-1] # Get the Last block
		last_hash = last_block.hash_block() # Get the hash of the last block

		nonce = self.proof_of_work() # Determine the nonce value

		# Create the reward and append it to the open transactions
		reward_transaction = Transaction(sender=None, recipient="recipient", book=None, transaction_type=2)
		self.open_transactions.append(reward_transaction)

		# Create the new Block
		new_block = Block(last_hash,self.open_transactions,index=len(self.block_chain),nonce=nonce)

		self.block_chain.append(new_block)

		self.open_transactions = []

	def to_json(self):
		"""
		to_json converts the object into a json object

		:var dict_json: contains information about the blocks
		:type dict_json: dict

		:returns: a dict (json) containing the chain
		:rtype: dict
		"""
		dict_json = {}

		# Loop through and convert the block to json objects
		for i, block in enumerate(self.block_chain):
			dict_json[i] = block.to_json()
		
		return dict_json

	# Returs number of block in the chain
	number_blocks = lambda self: len(self.block_chain)

	def __str__(self):
		print(f'::{self.number_blocks()} blocks in the blockchain')
		for block, number in zip(self.block_chain, range(len(self.block_chain))):
			print('number\n',number)
			print('block\n', block)
		return ''

if __name__ == '__main__':
	#Exemple on how to use the blockchain object
	blockchain = BlockChain()
	print(blockchain)
	blockchain.create_append_transaction(('mouha','recipient',Book(title='The Selfish Gene',author='Richard Dawkins', date='19--', genre='Science')))
	blockchain.mine_block('zeddo')
	print(blockchain)