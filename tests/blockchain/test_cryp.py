import sys
sys.path.append('../../')

import unittest
from modules.blockchain.cryp import Cryp
from fastecdsa.curve import secp256k1
from fastecdsa.point import Point
from fastecdsa import keys, ecdsa

class TestCryp(unittest.TestCase):

	def setUp(self):
		self.cryp = Cryp()
		self.private_key, self.public_key = keys.gen_keypair(secp256k1)

	def test_Cryp(self):
		self.assertEqual(self.cryp.path, '../../')
		self.assertIsNone(self.cryp.private_key)
		self.assertIsNone(self.cryp.public_key)
		cryp = Cryp(True)
		self.assertIsNotNone(cryp.private_key)
		self.assertIsNotNone(cryp.public_key)

	def test_generate_keys(self):
		self.cryp.generate_keys()
		self.assertIsInstance(self.cryp.private_key, int)
		self.assertGreaterEqual(len(str(self.cryp.private_key)), 70)
		self.assertIsNot(self.cryp.private_key, self.private_key)
		self.assertIsInstance(self.cryp.public_key, Point)
		self.assertTrue(self.cryp.public_key.curve == self.public_key.curve == secp256k1)

	def test_gen_privatekey(self):
		self.cryp.gen_privatekey()
		self.assertIsInstance(self.cryp.private_key, int)
		self.assertGreaterEqual(len(str(self.cryp.private_key)), 70)
		self.assertIsNot(self.cryp.private_key, self.private_key)

	def test_gen_publickey(self):
		with self.assertRaises(TypeError):
			self.cryp.gen_publickey()

		self.cryp.gen_publickey(self.private_key)
		self.assertIsInstance(self.cryp.public_key, Point)
		self.assertEqual(self.cryp.public_key, self.public_key)
		self.assertTrue(self.cryp.public_key.curve == self.public_key.curve == secp256k1)

	def test_export_keys(self):
		with self.assertRaises(TypeError):
			self.cryp.export_keys()

	def test_sign(self):
		with self.assertRaises(TypeError):
			self.cryp.sign("Test")

		self.cryp.private_key = self.private_key
		r, s = ecdsa.sign("Test", self.private_key, curve=secp256k1)
		self.assertEqual(self.cryp.sign("Test"), hex(r) + "," + hex(s))

	def test_get_signature(self):
		r, s = ecdsa.sign("Test", self.private_key, curve=secp256k1)
		self.assertEqual(Cryp.get_signature("Test", self.private_key), hex(r) + "," + hex(s))

	def test_verify_signature(self):
		self.cryp.generate_keys()
		signature_fastecda = ecdsa.sign("Test", self.private_key, curve=secp256k1)
		signature_cryp1 = Cryp.get_signature("Test", self.private_key)
		signature_cryp2 = Cryp.get_signature("Tests", self.cryp.private_key)

		self.assertEqual(signature_fastecda, tuple(map(lambda sig: int(sig, 0), signature_cryp1.split(','))))
		self.assertTrue(Cryp.verify_signature(self.public_key, signature_cryp1, "Test"))
		self.assertFalse(Cryp.verify_signature(self.public_key, signature_cryp1, "Tests"))
		self.assertFalse(Cryp.verify_signature(self.cryp.public_key, signature_cryp1, "Test"))
		self.assertFalse(Cryp.verify_signature(self.public_key, signature_cryp2, "Test"))

	def test_dump_pub(self):
		self.assertEqual(Cryp.dump_pub(self.public_key), hex(self.public_key.x) + "," + hex(self.public_key.y))

	def test_load_pub(self):
		public_key = hex(self.public_key.x) + "," + hex(self.public_key.y)
		self.assertEqual(Cryp.load_pub(public_key), self.public_key)