from OpenSSL import crypto
import os.path

class SPKeys():
	""" SPkey Object contains your own public and private keys, and sign given data """

	def __init__(self):
		"""Constructor of the class"""
		if os.path.isfile('private_key.pem') and os.path.isfile('public_key.pem'):
			print("HERE")

			with open('private_key.pem', 'rb') as f:
				private_key_data = f.read()

			with open('public_key.pem', 'rb') as f:
				public_key_data = f.read()

		else:
			print("NOPE!")
			key = crypto.PKey()
			key.generate_key(crypto.TYPE_RSA, 4096)

			private_key_data = crypto.dump_privatekey(crypto.FILETYPE_PEM, key)
			public_key_data = crypto.dump_publickey(crypto.FILETYPE_PEM, key)

			with open('private_key.pem', 'wb') as f:
				f.write(private_key_data)

			with open('public_key.pem', 'wb') as f:
				f.write(public_key_data)

		self.private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, private_key_data)
		self.public_key = crypto.load_publickey(crypto.FILETYPE_PEM, public_key_data)


	def sign(self, bite_data):
		""" sign given data (!data already converted to byte!) """
		signature = crypto.sign(self.private_key, bite_data, 'sha256')

		with open('signature.pem', 'wb') as f:
			f.write(signature)

		return signature
		