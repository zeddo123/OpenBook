import os
from OpenSSL import crypto

class OwnKeyMissing(Exception):
	"""Raised when the own pair private/public keys called but are missing"""
	pass

class Cryptog():
	""" SPkey Object contains your own public and private keys, and sign given data """

	def __init__(self):
		"""Constructor of the class"""

		dirpath = os.getcwd()
		self._dirpath = dirpath.replace('/modules/blockchain', '')

		if not(os.path.isdir('../../crypto')):
			os.mkdir('../../crypto')
			os.mkdir('../../crypto/.private')
			os.mkdir('../../crypto/public')
			os.mkdir('../../crypto/signature')
		else:
			if not(os.path.isdir('../../crypto/.private')):
				os.mkdir('../../crypto/.private')
			if not(os.path.isdir('../../crypto/public')):
				os.mkdir('../../crypto/public')

		self.private_key = None
		self.public_key = None

	def load_privatekey(self, generate=False):
		if not(generate):
			if os.path.isfile('../../crypto/.private/private_key.pem'):
				with open('../../crypto/.private/private_key.pem', 'rb') as f:
					private_key_data = f.read()
			else:
				raise OwnKeyMissing('private key not found')

		else:
			key = crypto.PKey()
			key.generate_key(crypto.TYPE_RSA, 4096)

			private_key_data = crypto.dump_privatekey(crypto.FILETYPE_PEM, key)
			public_key_data = crypto.dump_publickey(crypto.FILETYPE_PEM, key)

			with open('../../crypto/.private/private_key.pem', 'wb') as f:
				f.write(private_key_data)

			with open('../../crypto/public/public_key.pem', 'wb') as f:
				f.write(public_key_data)

		self.private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, private_key_data)


	def load_publickey(self, sender=None, own=True):
		if own:
			if os.path.isfile('../../crypto/public/public_key.pem'):
				with open('../../crypto/public/public_key.pem', 'rb') as f:
					public_key_data = f.read()
					self.public_key = crypto.load_publickey(crypto.FILETYPE_PEM, public_key_data)
			else:
				raise OwnKeyMissing('own public key not found')

		else:
			if os.path.isfile('../../crypto/public/'+sender+'.pem'):
				with open('../../crypto/public/'+sender+'.pem', 'rb') as f:
					public_key_data = f.read()
					self.public_key = crypto.load_publickey(crypto.FILETYPE_PEM, public_key_data)
			else:
				raise OwnKeyMissing('public key not found')

	def sign(self, bite_data):
		""" sign given data (!data already converted to byte!) """
		signature = crypto.sign(self.private_key, bite_data, 'sha256')

		if not(os.path.isdir('../../crypto/signature')):	
			os.mkdir('../../crypto/signature')

		with open('../../crypto/signature/signature.pem', 'wb') as f:
			f.write(signature)

		return signature
	
	@staticmethod
	def verify_signature(public_key, signature, bite_data):
		x509 = crypto.X509()
		x509.set_pubkey(public_key)
		try:
			if not(crypto.verify(x509, signature, bite_data, 'sha256')):
				return True
			else:
				return False
		except:
			return False



if __name__ == '__main__':
#	test
	k = Cryptog()
	k.load_privatekey(True)
	k.load_publickey()
	signature = k.sign(b"Hello WOrld")
	if Cryptog.verify_signature(k.public_key, signature, b"Hello WOrld"):
		print("signature Verified!")
	else:
		print("signature not valid!")