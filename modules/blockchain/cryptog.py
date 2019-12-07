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
		:type private_key: bytes.

		:attr public_key: the public key.
		:type public_key: bytes.

	:Methods:

		:meth gendir: Generate a Crypto Directory.

		:meth load_privatekey: Load the private key or generate a pair private/public keys.

		:meth load_publickey: Load the public key from the specified path.

		:meth set_publickey: Set the public key from buffer.

		:meth sign: Sign a byted data using self private key.

		:meth verify_signature: (staticmethod) Verify the signature for a data bytes.

	"""

	def __init__(self, path='../../'):
		self.path = path
		self.private_key = None
		self.public_key = None


	def generate_dir(self):
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


	def generate_keys(self, save=False, filen=None):
		"""
		Generate new Private and Public key pair.
		(optional) save keys in a pem file

		:param save: (optional) False to not save the new generated private/public key pair, 
					True to save them
		:type save: Boolean

		:param filen: (optional) is the pem file name of the public key to load, 
					if None load default public_key
		:type filen: str

		:return: None
		"""
		key = crypto.PKey()
		key.generate_key(crypto.TYPE_RSA, 4096)

		self.private_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, key)
		self.public_key = crypto.dump_publickey(crypto.FILETYPE_PEM, key)

		if save:
			if not filen:
				with open(self.path + 'crypto/.private/private_key.pem', 'wb') as f:
					f.write(self.private_key)

				with open(self.path + 'crypto/public/public_key.pem', 'wb') as f:
					f.write(self.public_key)

			else:
				with open(self.path + 'crypto/.private/'+filen+'prv.pem', 'wb') as f:
					f.write(self.private_key)

				with open(self.path + 'crypto/public/'+filen+'pub.pem', 'wb') as f:
					f.write(self.public_key)


	def load_privatekey(self, filen=None):
		"""
		Load the private key or generate a pair private/public keys.

		:param filen: (optional) is the pem file name of the public key to load, 
					if None load default public_key
		:type filen: str

		:return: None
		"""
		if not filen:
			if os.path.isfile(self.path + 'crypto/.private/private_key.pem'):
				with open(self.path + 'crypto/.private/private_key.pem', 'rb') as f:
					private_key_data = f.read()

			else:
				raise CryptoKeyMissing('private key not found')

		else:
			if os.path.isfile(self.path + 'crypto/.private/'+filen+'prv.pem'):
				with open(self.path + 'crypto/.private/'+filen+'prv.pem', 'rb') as f:
					private_key_data = f.read()

			else:
				raise CryptoKeyMissing('private key not found')

		self.private_key = private_key_data


	def load_publickey(self, filen=None):
		"""
		Load the public key from the specified path.

		:param filen: (optional) is the pem file name of the public key to load, 
					if None load default public_key
		:type filen: str

		:return: None
		"""
		if not filen:
			if os.path.isfile(self.path + 'crypto/public/public_key.pem'):
				with open(self.path + 'crypto/public/public_key.pem', 'rb') as f:
					public_key_data = f.read()

			else:
				raise CryptoKeyMissing('own public key not found')

		else:
			if os.path.isfile(self.path + 'crypto/public/'+filen+'pub.pem'):
				with open(self.path + 'crypto/public/'+filen+'pub.pem', 'rb') as f:
					public_key_data = f.read()
					
			else:
				raise CryptoKeyMissing('public key not found')

		self.public_key = public_key_data


	def set_publickey(self, pkey, byte=False):
		"""
		Set the public key from buffer.

		:param pkey: The public key.
		:type pkey: :py:class:`PKey / bytes.

		:param byte: (optional) False means key is a PKey instance, 
					True means key is byte.
		:type byte: boolean

		:return: None
		"""
		if byte == False:
			if not isinstance(pkey, crypto.PKey):
				raise TypeError("pkey must be a PKey instance")

			else:
				pkey = crypto.dump_publickey(crypto.FILETYPE_PEM, pkey)

		elif byte != True:
			raise TypeError('byte must be Boolean')

		self.public_key = pkey #TODO: Add verification for byted key


	def sign(self, data, save=False, filen=None):
		"""
		Sign a byted data using self private key.
		(optional) save signature in a pem file.

		:param data: data to be signed
		:type data: bytes
		
		:param save: (optional) True to save the signature on a pem file into the self path,
					False to not save it
		:type save: boolean

		:param filen: (optional) is the pem file name of the public key to load, 
					if None load default public_key.
		:type filen: str

		:return: signature
		:rtype: bytes
		"""
		private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, self.private_key)
		signature = crypto.sign(private_key, data, 'sha256')

		if save:
			if not filen:
				with open(self.path + 'crypto/signature/signature.pem', 'wb') as f:
					f.write(signature)

			else:
				with open(self.path + 'crypto/signature/'+filen+'sig.pem', 'wb') as f:
					f.write(signature)

		return signature


	@staticmethod
	def get_signature(private_key, data, byte=False):
		"""
		Sign a byted data using given private key.
		
		:param private_key: private key
		:type public_key: :py:class:`PKey / bytes.
		d
		:param data: data to be signed
		:type data: bytes

		:param byte: (optional) False means key is a PKey instance, 
					True means key is byte.
		:type byte: boolean

		:return: signature
		:rtype: bytes
		"""
		if byte == False:
			private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, private_key)

		elif byte != True:
			raise TypeError('byte must be Boolean')

		if not isinstance(private_key, crypto.PKey):
			raise TypeError("pkey must be a PKey instance")

		signature = crypto.sign(private_key, data, 'sha256')
		return signature
	

	@staticmethod
	def verify_signature(public_key, signature, data, byte=False):
		"""
		Verify the signature for a data bytes.

		:param public_key: the public key corresponding to the
        				private key which generated the signature
        :type public_key: :py:class:`PKey / bytes.

        :param signature: signature returned by sign method
        :type signature: bytes

        :param data: data to be verified
        :type data: bytes

        :param byte: (optional) False means key is a PKey instance, 
					True means key is byte.
		:type byte: boolean

        :return: ''True'' if signature is valid, ''False'' otherwise
        :rtype: boolean
		"""
		if byte == False:
			public_key = crypto.load_publickey(crypto.FILETYPE_PEM, public_key)

		elif byte != True:
			raise TypeError('byte must be Boolean')

		if not isinstance(public_key, crypto.PKey):
			raise TypeError("pkey must be a PKey instance")

		else:
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