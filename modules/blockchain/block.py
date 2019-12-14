import datetime
import json

from modules.blockchain.transaction import *


class Block:
    """Block Object to be added to the chain

    :Attributes:

        :attr previous_hash: The previous hash of the block
        :type previous_hash: str

        :attr transactions: All the transactions in the block
        :type transactions: list

        :attr index: The number of the block in the chain
        :type index: int

        :attr nonce: The nonce of the block **by default like bitcoin**
        :type nonce: int

        :attr timestamp: The time in witch the block was created
        :type timestamp: str

    :Methods:

        :meth __init__: Constructor of the class
        :meth to_json: Create a json file of the block
        :meth hash_block: Calculate the hash of the block
        :meth __str__: magic method, prints the block

    """

    def __init__(self, previous_hash=None, transactions=[], index=0, nonce=208393, override=False):
        """Block class constructor
        :param previous_hash: The previous hash of the block
        :type previous_hash: str

        :param transactions: All the transcations in the block
        :type transactions: list

        :param index: The number of the block in the chain
        :type index: int

        :param nonce: The nonce of the block **by default like bitcoin**
        :type nonce: int
        """
        self.previous_hash = previous_hash
        self.index = index
        self.transactions = list(transactions)
        self.nonce = nonce
        self.timestamp = self.date_time_now() if not override else None
        self.hash = self.hash_block() if not override else None

    @staticmethod
    def date_time_now():
        """ date_time_now returns the current precise date and time as a string """
        return datetime.datetime.now().__str__()

    def to_json(self, hash=False) -> dict:
        """
        to_json converts the object into a json object

        :var json_dict: contains information about the block

        1. previous hash
        2. index
        3. transactions
        4. nonce
        5. Time-stamp

        :var json_dict: dict
        :returns: a dict (json) containing of the information of the block
        :rtype: dict
        """
        json_dict = {
            'previous_hash': self.previous_hash,
            'index': self.index,
            'transactions': list(map(Transaction.to_json, self.transactions)),
            'nonce': self.nonce,
            'Timestamp': self.timestamp
        }

        if not hash:
            json_dict['hash'] = self.hash

        return json_dict

    def hash_block(self) -> str:
        """hash_block calculate the hash of the block
        :returns: hash of the block
        :rtype: str
        """
        return hashlib.sha256(json.dumps(self.to_json(hash=True)).encode()).hexdigest()

    def __eq__(self, other):
        return self.to_json() == other.to_json()

    def __repr__(self):
        return str(self.to_json())

    def __str__(self):
        """__str__ return the json object to be printed
        :returns: text json object
        :rtype: str
        """
        return str(self.to_json())

    @staticmethod
    def json_to_block(b_json):
        bk = Block(transactions=[], override=True)
        for key, val in b_json.items():
            if key == 'transactions':
                # When converting the json object to a bk
                # Converting all the transaction to Transaction object is necessary
                for i in val:
                    bk.transactions.append(Transaction.json_to_transaction(i))
            else:
                setattr(bk, key.lower(), val)

        return bk
