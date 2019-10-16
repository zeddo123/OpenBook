import hashlib


class Transaction:
	"""
		docstring for Transaction
		type:
			1 for the transaction of "Book"
			2 for the transaction of mining
	"""
	def __init__(self, sender, recipient, book, transaction_type=1):
		self.type = transaction_type
		self.sender = sender if self.type == 1 else 'mining'
		self.recipient = 'data-base' if self.type == 1 else recipient
		self.book = book if self.type == 1 else None #TODO: {'FRIEND NOTICE': optimisation}, usless repetion of the same "if" condition (line 15 and line 23)

	
	def to_json(self):
		json_dict = {
			'type': self.type,
			'sender': self.sender,
			'recipient': self.recipient,
			'book': self.book.to_json() if self.type == 1 else None #TODO: {'FRIEND NOTICE': optimisation}, usless repetion of the same "if" condition (line 15 and line 23)
		}
		return json_dict