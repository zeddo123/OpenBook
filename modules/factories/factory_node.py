from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet import reactor

import sys
sys.path.insert(0, '..')

from modules.utils import uuid_generator
from modules.protocols.protocol_node import *
from modules.blockchain.blockchain import *


class P2PFactory(Factory):
	"""docstring for P2PFactory"""
	
	def __init__(self, port, max_peers=0, debug=True):
		self.blockchain = BlockChain()
		# debug variable if True prints log
		self.debug = debug

		# active variable, if True the peer is still running
		self.active = True

		# max_peers is the number of peers the peers can handle
		self.max_peers = max_peers
		# Get the listening port
		self.port = port

		self.uuid = uuid_generator()
		
		# dict of all the peers that are connected to this node
		self.known_peers = {}

		# List of all the peers that the current node will connect-to as a `client`
		self.server_peers = []

		#Connect to the SeedSever
		seed_point = TCP4ClientEndpoint(reactor, "localhost", 5989)
		self.seed_connection = connectProtocol(seed_point, P2Protocol(self, node_type=2))

		# Initiate handshake with seed server
		self.update_peers()

	def _debug(self, msg):
		if self.debug: print(msg)

	
	def update_peers(self):
		# Send Request to get new_peers from seed server
		self.seed_connection.addCallback(lambda p : p.send_handshake())



	def buildProtocol(self, addr):
		return P2Protocol(self)
