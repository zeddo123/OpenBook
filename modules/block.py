import hashlib
import json
import datetime
from transaction import *


class Block:
	"""docstring for Block"""
	def __init__(self, previous_hash=None, transactions=[], index=0, nonce=208393):
		self.previous_hash = previous_hash
		self.index = index
		self.transactions = transactions
		self.nonce = nonce
		self.timestamp = datetime.datetime.now().__str__() 

	def to_json(self):
		json_dict = {
			'previous_hash': self.previous_hash,
			'index': self.index,
			'transactions': list(map(Transaction.to_json,self.transactions)),
			'nonce': self.nonce,
			'Timestamp': self.timestamp
		}
		return json_dict

	def hash_block(self):
		return hashlib.sha256(json.dumps(self.to_json()).encode()).hexdigest()

	def __str__(self):
		return str(self.to_json())