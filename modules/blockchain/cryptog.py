import os
from OpenSSL import crypto

class CryptoKeyMissing(Exception):
	"""
	Raised when the own pair private/public keys called but are missing.
	"""
	pass

class CryptoError(Exception):
	"""
	Raised when a crypto error has occurred.
	"""
	pass

class Cryptog():
	""" 
	A class representing an RSA private/public key or key pair.

	:Attributes:

		:attr path: a directory path to load from and save on.
		:type path: str
		
		:attr private_key: the private key.
		:type private_key: :py:class:`PKey.

		:attr public_key: the public key.
		:type public_key: :py:class:`PKey.

	:Methods:

		:meth gendir: Generate a Crypto Directory.

		:meth load_privatekey: Load the private key or generate a pair private/public keys.

		:meth load_publickey: Load the public key from the specified path.

		:meth set_publickey: Set the public key from buffer.

		:meth sign: Sign a byted data using self private key.

		:meth verify_signature: (staticmethod) Verify the signature for a data bytes.

	"""

	def __init__(self, path='../../'):
		"""Constructor of the class"""
		self.path = path
		self.private_key = None
		self.public_key = None


	def gendir(self):
		"""
		Generate a Crypto Directory.
		"""
		if not(os.path.isdir(self.path + 'crypto')):
			os.mkdir(self.path + 'crypto')
			os.mkdir(self.path + 'crypto/.private')
			os.mkdir(self.path + 'crypto/public')
			os.mkdir(self.path + 'crypto/signature')
		else:
			if not(os.path.isdir(self.path + 'crypto/.private')):
				os.mkdir(self.path + 'crypto/.private')
			if not(os.path.isdir(self.path + 'crypto/public')):
				os.mkdir(self.path + 'crypto/public')
			if not(os.path.isdir(self.path + 'crypto/signature')):	
				os.mkdir(self.path + 'crypto/signature')


	def load_privatekey(self, generate=False, save=False):
		"""
		Load the private key or generate a pair private/public keys.

		:param generate: (optional) False to lead the key from the specified path, 
						True to generate new private/public key pair.
		:type generate: Boolean.

		:param save: (optional) False to not save the new generated private/public key pair, 
					True to save them.
		:type save: Boolean.

		:return: None
		"""
		if not generate:
			if os.path.isfile(self.path + 'crypto/.private/private_key.pem'):
				with open(self.path + 'crypto/.private/private_key.pem', 'rb') as f:
					private_key_data = f.read()
			else:
				raise CryptoKeyMissing('private key not found')

		else:
			key = crypto.PKey()
			key.generate_key(crypto.TYPE_RSA, 4096)

			private_key_data = crypto.dump_privatekey(crypto.FILETYPE_PEM, key)
			public_key_data = crypto.dump_publickey(crypto.FILETYPE_PEM, key)

			if save:
				with open(self.path + 'crypto/.private/private_key.pem', 'wb') as f:
					f.write(private_key_data)

				with open(self.path + 'crypto/public/public_key.pem', 'wb') as f:
					f.write(public_key_data)

		self.private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, private_key_data)
		self.public_key = crypto.load_publickey(crypto.FILETYPE_PEM, public_key_data)


	def load_publickey(self, filen=None):
		"""
		Load the public key from the specified path.

		:param filen: (optional) is the pem file name of the public key to load, 
					if None load default public_key.
		:type filen: str.

		:return: None.
		"""
		if not filen:
			if os.path.isfile(self.path + 'crypto/public/public_key.pem'):
				with open(self.path + 'crypto/public/public_key.pem', 'rb') as f:
					public_key_data = f.read()
					self.public_key = crypto.load_publickey(crypto.FILETYPE_PEM, public_key_data)
			else:
				raise CryptoKeyMissing('own public key not found')

		else:
			if os.path.isfile(self.path + 'crypto/public/'+filen+'.pem'):
				with open(self.path + 'crypto/public/'+filen+'.pem', 'rb') as f:
					public_key_data = f.read()
					self.public_key = crypto.load_publickey(crypto.FILETYPE_PEM, public_key_data)
			else:
				raise CryptoKeyMissing('public key not found')


	def set_publickey(self, pkey, byte=False):
		"""
		Set the public key from buffer.

		:param pkey: The public key.
		:type pkey: :py:class:`PKey.

		:param byte: (optional) False means key is a PKey instance, 
					True means key is byte.
		:type byte: boolean

		:return: None
		"""
		if byte:
			try:
				self.public_key = crypto.load_publickey(crypto.FILETYPE_PEM, pkey)

			except OpenSSL.crypto.Error:
				raise CryptoError('Invalid byte key')

		elif not byte:
			if not isinstance(pkey, crypto.PKey):
				raise TypeError("pkey must be a PKey instance")

			else:
				self.public_key = pkey

		else:
			raise TypeError('byte must be Boolean')


	def sign(self, data, save=False):
		"""
		Sign a byted data using self private key.

		:param data: data to be signed
		:type data: bytes
		
		:param save: (optional) True to save the signature on a pem file into the self path,
					False to not save it
		:type save: boolean

		:return: signature
		:rtype: bytes
		"""
		signature = crypto.sign(self.private_key, data, 'sha256')

		if save:
			with open(self.path + 'crypto/signature/signature.pem', 'wb') as f:
				f.write(signature)

		return signature

	
	@staticmethod
	def verify_signature(public_key, signature, data):
		"""
		Verify the signature for a data bytes.

		:param public_key: the public key corresponding to the
        				private key which generated the signature
        :type public_key: :py:class:`PKey

        :param signature: signature returned by sign method
        :type signature: bytes

        :param data: data to be verified
        :type data: bytes

        :return: ''True'' if signature is valid, ''False'' otherwise
        :rtype: boolean
		"""
		x509 = crypto.X509()
		x509.set_pubkey(public_key)
		try:
			if not(crypto.verify(x509, signature, data, 'sha256')):
				return True
			else:
				return False
		except:
			return False



if __name__ == '__main__':
#	test
	k = Cryptog()
	k2 = Cryptog()
	k3 = Cryptog()

	k.gendir()
	k.load_privatekey(generate=True, save=True)

	k2 = Cryptog()
	k2.load_publickey()

	k3.set_publickey(k.public_key)

	signature = k.sign(b"Hello WOrld")

	if (Cryptog.verify_signature(k.public_key, signature, b"Hello WOrld") 
		and Cryptog.verify_signature(k2.public_key, signature, b"Hello WOrld") 
		and Cryptog.verify_signature(k3.public_key, signature, b"Hello WOrld")):

		print("signature Verified!")
	else:
		print("signature not valid!")