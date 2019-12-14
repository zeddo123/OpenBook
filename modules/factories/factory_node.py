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
	"""P2PFactory
	:Attributes:
		:blockchain: the blockchain object of the node
		:debug: a debug attribute, used to print helpful messages
		:active: The state of the node -in general
		:max_peers: the maximum number of peers the node can connect-to
		:port: the listening port of the node
		:uuid: the universal identifier of the node
		:known_peers: all the know_peers
		:server_peers: all the peers which the current node connected-to as a client
		:seed_point: the clientEndpoint to connect to the seed server
	"""
	
	def __init__(self, port, max_peers=0, debug=True):
		self.blockchain = BlockChain()
		# blockchain buffer will contain a temporary list of blockchains 
		self._blockchain_buffer = []
		
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
		seed_point = TCP4ClientEndpoint(reactor, "localhost", 5000)
		self.seed_connection = connectProtocol(seed_point, P2Protocol(self, node_type=2))

		# Initiate handshake with seed server
		self.update_peers()

	def update_peers(self):
		# Send Request to get new_peers from seed server
		self.seed_connection.addCallback(lambda p : p.send_handshake())

	def dispatch_get_blockchain(self, protocol):
		# Send a get_blockchain request except for the node who started the feed-back
		for id,p in know_peers.items():
			if p != protocol:
				p.send_get_blockchain()

	def dispatch_blockchain(self, protocol, bc):
		for id,p in know_peers.items():
			if p != protocol:
				p.send_blockchain(bc)

	def buildProtocol(self, addr):
		return P2Protocol(self)
