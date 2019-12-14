import os
from fastecdsa.curve import secp256k1
from fastecdsa import keys, ecdsa


class Cryp():
	""" 
	A class representing an ECDSA secp256k1 private/public key or key pair.

	:Attributes:

		:attr path: a directory path to load from and save on.
		:type path: str
		
		:attr private_key: the private key.
		:type private_key: int.

		:attr public_key: the public key.
		:type public_key: int.

	:Methods:

		:meth gendir: Generate a Crypto Directory.

		:meth generate_keys: Generate new Private and Public key pair.

		:meth gen_privatekey: Generate new Private key.

		:meth gen_publickey: Get public key from private key.

		:meth export_keys: Save keys to disk.

		:meth import_keys: import the private and public key from disk.

		:meth import_publickey: import the public key from disk.

		:meth sign: Sign data using self private key.

		:meth verify_signature: (staticmethod) Verify the signature of a data.

	"""

	def __init__(self, path='../../'):
		self.path = path
		self.private_key = None
		self.public_key = None


	def generate_dir(self):
		"""
		Generate a Crypto Directory.

		:return: None
		"""
		if not(os.path.isdir(self.path + 'cryp')):
			os.mkdir(self.path + 'cryp')
			os.mkdir(self.path + 'cryp/.private')
			os.mkdir(self.path + 'cryp/public')
			os.mkdir(self.path + 'cryp/signature')
		else:
			if not(os.path.isdir(self.path + 'cryp/.private')):
				os.mkdir(self.path + 'cryp/.private')
			if not(os.path.isdir(self.path + 'cryp/public')):
				os.mkdir(self.path + 'cryp/public')
			if not(os.path.isdir(self.path + 'cryp/signature')):	
				os.mkdir(self.path + 'cryp/signature')


	def generate_keys(self, save=False, filen='default_key'):
		"""
		Generate new Private and Public key pair.
		(optional) save keys in a pem file

		:param save: (optional) False to not save the new generated private/public key pair, 
					True to save them
		:type save: Boolean

		:param filen: (optional) is the pem file name of key to load
		:type filen: str

		:return: None
		"""
		self.private_key, self.public_key = keys.gen_keypair(secp256k1)

		if save:
			keys.export_key(self.private_key, curve=secp256k1, filepath=self.path + 'cryp/.private/'+filen+'prv.pem')
			keys.export_key(self.public_key, curve=secp256k1, filepath=self.path + 'cryp/public/'+filen+'pub.pem')


	def gen_privatekey(self):
		"""
		Generate new Private key.

		:return: None
		"""
		self.private_key = keys.gen_private_key(secp256k1)

	def gen_publickey(self, key=None):
		"""
		Get public key from private key.

		:param key: (optional) the private key
		:type key: int

		:return: None
		"""
		if key:
			self.public_key = keys.get_public_key(key, secp256k1)
		elif self.private_key: 
			self.public_key = keys.get_public_key(self.private_key, secp256k1)
		else:
			raise TypeError("no private key to generate from")


	def export_keys(self, filen='default_key'):
		"""
		Save keys to disk.

		:param filen: (optional) is the pem file name of key to load
		:type filen: str

		:return: None
		"""
		if not self.private_key and not self.public_key:
			raise TypeError("no key to export")

		if self.private_key:
			keys.export_key(self.private_key, curve=secp256k1, filepath=self.path + 'cryp/.private/'+filen+'prv.pem')

		if self.public_key:
			keys.export_key(self.public_key, curve=secp256k1, filepath=self.path + 'cryp/public/'+filen+'pub.pem')
					

	def import_keys(self, filen='default_key'):
		"""
		import the private and public key from disk.

		:param filen: (optional) is the pem file name of key to load
		:type filen: str

		:return: None
		"""
		self.private_key, self.public_key = keys.import_key(self.path + 'cryp/.private/'+filen+'prv.pem', curve=secp256k1)


	def import_publickey(self, filen='default_key'):
		"""
		import the public key from disk.

		:param filen: (optional) is the pem file name of key to load
		:type filen: str

		:return: None
		"""
		self.public_key = keys.import_key(self.path + 'cryp/public/'+filen+'pub.pem', curve=secp256k1, public=True)


	def sign(self, data):
		"""
		Sign data using self private key.

		:param data: data to be signed
		:type data: str

		:return: signature
		:rtype: tuple
		"""
		if self.private_key:
			signature = ecdsa.sign(data, self.private_key, curve=secp256k1)
		else:
			raise TypeError("no private key to sign with")

		return signature

	@staticmethod
	def get_signature(data, key):
		"""
		Sign data using self private key.

		:param data: data to be signed
		:type data: str

		:param key: The private key
		:type key: int

		:return: signature
		:rtype: tuple
		"""
		return ecdsa.sign(data, key, curve=secp256k1)

	@staticmethod
	def verify_signature(public_key, signature, data):
		"""
		Verify the signature of a data.

		:param public_key: the public key corresponding to the
        				private key which generated the signature
		:type public_key: Point

		:param signature: signature returned by the sign method
		:type signature: tuple

		:param data: data to be verified
		:type data: str

		:return: ''True'' if signature is valid, ''False'' otherwise
		:rtype: boolean
		"""
		return ecdsa.verify(signature, data, public_key, curve=secp256k1)


if __name__ == '__main__':
#	test
	k = Cryp()
	k2 = Cryp()
	k3 = Cryp()

	k.generate_dir()
	k.generate_keys(save=True)

	k2.import_keys()
	k3.import_publickey()

	signature1 = k.sign("Hello WOrld")
	signature2 = Cryp.get_signature("Hello Worlds", k2.private_key)

	if (Cryp.verify_signature(k.public_key, signature1, "Hello WOrld") 
		and Cryp.verify_signature(k2.public_key, signature1, "Hello WOrld") 
		and Cryp.verify_signature(k3.public_key, signature2, "Hello Worlds")):

		print("signature Verified!")
	else:
		print("signature not valid!")