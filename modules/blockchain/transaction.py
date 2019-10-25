import hashlib


class Transaction:
	"""
	the transaction object contains all the information about a transaction

	Attributes
	==========
	
	:attr transaction_type: type tells us if a transaction if a reward one or not
	if it's the case,no need to create a book object
	:type transaction_type: int

	* 1 -> for a "Book" transaction 
	* 2 -> for a reward transaction


	:attr sender: the name/id of the node creating the transaction
	:type sender: str

	:attr recipient: depending on the type of transaction.the recipient can be
	the block-chain or the miner in the case of a `reward transaction`
	:type recipient: str

	:attr book: the book that will be stored in the transaction *(if type == 1)*
	:type book: book object `book.py`

	Methods
	=======

	:meth __init__: Constructor of the object
	:meth to_json: returns a *dict* containing all the information

	"""
	def __init__(self, sender, recipient, book, transaction_type=1):
		self.type = transaction_type
		self.sender = sender if self.type == 1 else 'mining'
		self.recipient = 'the-chain' if self.type == 1 else recipient
		self.book = book.to_json() if self.type == 1 else None

	
	def to_json(self):
		json_dict = {
			'type': self.type,
			'sender': self.sender,
			'recipient': self.recipient,
			'book': self.book
		}
		return json_dict

	@classmethod
	def json_to_transaction(json_transaction):
		"""Convert a json/dict into a Transaction object
		
		[description]
		:param json_transaction: transaction
		:type json_transaction: json/dict
		:returns: The converted transaction
		:rtype: Transaction
		"""
		sender = json_transaction['sender']
		type_t = json_transaction['type']
		recipient = json_transaction['recipient']
		book = json_transaction['book']
		
		return Transaction(sender,recipient,book,type_t)