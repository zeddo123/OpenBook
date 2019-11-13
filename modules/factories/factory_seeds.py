from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

import sys
sys.path.insert(0, '..')

from modules.protocols.protocol_seeds import *


class SeedFactory(Factory):
	"""SeedFactory is typical factory object
	returns a SeedProtocol instance when a connection is made
	:Attributes:
		:debug: a debug attribute, used to print helpful messages
		:known_peers: a dict that stores all the remote nodes
	"""
	def __init__(self, debug=True):
		# debug variable if True prints log
		self.debug = debug

		self.known_peers = {}

	def buildProtocol(self, addr):
		return SeedProtocol(self)
