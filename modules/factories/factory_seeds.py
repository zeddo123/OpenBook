from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

import sys
sys.path.insert(0, '..')

from modules.protocols.protocol_seeds import *


class SeedFactory(Factory):
	"""docstring for P2PFactory"""
	def __init__(self, debug=True):
		# debug variable if True prints log
		self.debug = debug

		self.known_peers = {}


	def _debug(self, msg):
		if self.debug: print(msg)
	
	
	def buildProtocol(self, addr):
		return SeedProtocol(self)
