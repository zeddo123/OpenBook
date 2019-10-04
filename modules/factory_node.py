from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet import reactor

from .utils import uuid_generator
from .protocol_node import *
from .blockchain import *


class P2PFactory(Factory):
	"""docstring for P2PFactory"""
	def __init__(self, port, max_peers=0, debug=True):
		self.blockchain = BlockChain()
		# debug variable if True prints log
		self.debug = debug

		# active variable, if True the peer is still running
		self.active = True

		# max_peers is the number of peers the peers can handel
		self.max_peers = max_peers
		# Get the lisening port
		self.port = port

		self.uuid = uuid_generator()
		self.known_peers = {}

		#Connect to the SeedSever
		seed_point = TCP4ClientEndpoint(reactor, "localhost", 5989)
		self.seed_connection = connectProtocol(seed_point, P2Protocol(self, node_type=2))
		self.update_peers(first_time=True)

	def _debug(self, msg):
		if self.debug: print(msg)

	
	def update_peers(self, first_time=False):
		# Send Request to get new_peers from seed server
		if first_time == True:
			self.seed_connection.addCallback(lambda p : p.send_handshake())
			self.seed_connection.addCallback(lambda p : p.send_get_blockchain())
		else:
			self.seed_connection.addCallback(lambda p : p.send_get_peers())


	def buildProtocol(self, addr):
		return P2Protocol(self)