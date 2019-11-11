# Imports from the twisted module
from twisted.internet.protocol import Protocol
from twisted.internet.task import LoopingCall
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet import reactor

# Import from standard modules
from time import time
from operator import xor
import json
from pprint import pprint as pp
from termcolor import colored

# Import from custom modules
import sys
sys.path.insert(0, '..')

from modules.utils import max_pow_2
from modules.blockchain.transaction import Transaction
from modules.protocols.protocol_client import ClientProtocol


class P2Protocol(ClientProtocol):
	"""
		the peer-2-peer protocol
		
		:Attributes:
			:attr node_type:
				1. Server instance of P2Protocol
				2. client instance of P2Protocol
			:type node_type: int
			:attr state: the state of the protocol instance *("waiting" or "active")*
			:type state: str
			:attr factory: the node-factory object for interacting with global variables
			:type factory: factory
			:attr my_ip: the ip address of the current node
			:type my_ip: str
			:attr my_port: the ip port of the current node
			:type my_port: int
			:attr nodeid: the nodeid *uuid* of the current node
			:type nodeid: str
			:attr remote_nodeid: the nodeid *uuid* of the connected-to node
			:type remote_nodeid: str
			:attr loop_ping: a loopingCall to start pinging every 5 minutes
			:type loop_ping: LoopingCall *twisted.internet.task*
			:attr last_ping: Last time the node sent a ping
			:type last_ping: int
		:Methods:
			:Twisted specific:
				:meth connectionMade: triggered when the connection is made **Override from ClientProtocol**
				:meth connectionLost: triggered when the connection is lost **Override from ClientProtocol**
				:meth dataReceived: every time a data is received, this method is called **Override from ClientProtocol**
			:Handling Initialisation:
				:meth handel_pong: called when a pong is received **Override from ClientProtocol**
				:meth send_handshake: Send all the informations about the node **Override from ClientProtocol**
				:meth handel_handshake: called when a handshake is received
			:Getting new peers:
				:meth handel_post_peers: called when new peers are received **Override from ClientProtocol**
			:Sending/Posting/Handling the block-chain:
				:meth send_get_blockchain: Sends a *"get block-chain request"* to receive the node's chain
				:meth send_blockchain: Sends the local chain
				:meth handel_blockchain: called whenever a block-chain is received
			:Sending/Posting/Handling the transactions:
				:meth send_transaction: Sends a transaction
				:meth handel_transaction: called whenever a transaction is received
			:Starting a client instance:
				:meth connect_to: This method connect to a node *'as a client'*
			:Debug Mode:
				:meth _debug: Prints helpful information **Override from ClientProtocol**
	"""
	def __init__(self, factory, node_type=1):
		self.state = 'waiting'
		self.factory = factory
		#uuid of the node
		self.my_ip = None
		self.my_port = factory.port
		self.nodeid = factory.uuid
		self.node_type = node_type
		
		#Connected Node
		self.remote_nodeid = None
		#Looping call to ping the connected nodes
		self.loop_ping = LoopingCall(self.send_ping) 
		self.last_ping = None

		ClientProtocol.__init__(self)


	def connectionMade(self):
		self._debug(f'{ "<-" if self.node_type == 1 else "->" }Connection Made with {self.transport.getPeer()}')
		self.my_ip = self.transport.getHost().host

	def connectionLost(self, reason):
		self._debug(f'Connection Lost with {self.remote_nodeid} {reason}')
		if self.remote_nodeid in self.factory.known_peers:
			self.factory.known_peers.pop(self.remote_nodeid)
			if self.loop_ping.running == True:
				self.loop_ping.stop()


	def dataReceived(self, data):
		self._debug(f'---------------Received Data---------------')
		
		for line in data.decode('utf-8').splitlines():
			
			line = line.strip()
			current_data = json.loads(line)
			self._debug(current_data, pprint=True)

			info_type = current_data['information_type'] # Get the type of the request

			if info_type == 'handshake' and self.state != 'Active':
				self.handel_handshake(line)
				self.state = 'Active'
			
			elif info_type == 'ping':
				self.send_pong()
			elif info_type == 'pong':
				self.handel_pong(line)
			
			elif info_type == 'post_peers':
				self.handel_post_peers(line)
			
			elif info_type == 'get_blockchain':
				self.send_blockchain()
			elif info_type == 'post_blockchain':
				pass
			
			elif info_type == 'get_transaction':
				pass
			elif info_type == 'post_transaction':
				self.handel_transaction(line)

		self._debug('__________________________________________\n\n\n\n')

	# Handling Initialisation
	def handel_pong(self, pong):
		"""when receiving a pong we are sure that the node is alive
		
		we print a msg *(in debug mode)* notifing that the node is alive
			and we save the time at which the pong was received
		
		:param pong: the msg received
		:type pong: str

		*Override method from ClientProtocol*
		"""
		self._debug(f'Node {self.remote_nodeid} still active ::{pong}')
		self.last_ping = time()

	def send_handshake(self):
		"""Sends a handshake to the new connection
		
		:var hs: contains the handshake request with all the information concerning the node
			* information_type
			* nodeid
			* ip of the node
			* port of the node

		:type hs: json
		
		*Override method from ClientProtocol*
		"""
		self._debug(f'Sending handshake {self.transport.getPeer()}')
		hs = json.dumps({
						'information_type': 'handshake',
						'nodeid': self.nodeid,
						'my_ip': self.my_ip,
						'my_port': self.my_port
						})
		self.transport.write((hs+'\n').encode())	

	def handel_handshake(self, hs):
		"""deals with what to do when a handshake is received

		:param hs: handshake
		:type hs: Json/dict
		"""

		hs = json.loads(hs)
		# Get the remote node id (uuid) from handshake
		self.remote_nodeid = hs['nodeid']

		if self.remote_nodeid == self.nodeid:
			self._debug('Oups, Connected to myself')
			self.transport.loseConnection()
		else:
			self.factory.known_peers[self.remote_nodeid] = self
			
			# Resend a handshake and connect as a client only 
			# if protocol instance is a server
			if self.node_type == 1 and not self.remote_nodeid in self.factory.server_peers:
				self.send_handshake()
			
			if not self.remote_nodeid in self.factory.server_peers:
				self.factory.server_peers.append(self.remote_nodeid)
				self.connect_to(ip=hs['my_ip'], port=hs['my_port'])

			if self.loop_ping.running == False and self.node_type == 1:
				self._debug('Looping Call started')
				self.loop_ping.start(60 * 5) # Start pinging every 5 mins

	# Getting new peers
	def handel_post_peers(self, peers):
		"""deals with what to 
		do when a new list of node is received
		
		loop through the peers and connect to them by following the kademlia routing table

		:param peers: list of new peers
		:type peers: json/dict
		
		*@override from ClientProtocol*
		"""
		peers = json.loads(peers)
		number_queue = peers['number_queue']
		self.remote_nodeid = peers['nodeid']

		for rank, peer in peers['known_peers'].items():
			peer = peer.split(':')
			ip = peer[1]
			port = peer[2]
			
			# Creating A connection following Kademlia RT
			if xor(int(number_queue),int(rank)) in max_pow_2(len(peers['known_peers'])+1):
				self._debug('Found New Node :: Connecting')
				self.connect_to(ip,port)


	# Sending/Posting/Handling the block-chain
	def send_get_blockchain(self):
		"""The method that sends a request to get a chain"""

		block_json = json.dumps({'information_type': 'get_blockchain'})
		self._debug(f'Send get_blockchain request {self.remote_nodeid}')
		self.transport.write((block_json + '\n').encode())

	def send_blockchain(self):
		"""sends the local chain to the connected node

		:var serial_block: contains the local blockchain and information_type tag next to it
		:serial_block: json
		"""
		serial_block = json.dumps({
									'information_type': 'post_blockchain',
									'blockchain': self.factory.blockchain.to_json()
								})
		self.transport.write(serial_block)

	def handel_blockchain(self, blockchain):
		"""deals with what to do when a block-chain is received
		
		if the received blockchain is longer then we update the local one

		:param blockchain: the new chain
		:type blockchain: json/dict

		"""
		blockchain = json.loads(blockchain)['blockchain']
		if blockchain.number_blocks() > self.factory.blockchain.number_blocks():
			self.factory = blockchain
			self._debug('-> Updating Local Blockchain')
		else:
			self._debug('-> Updating Local Blockchain -> Local Blockchain longer')


	# Sending/Posting/Handling the transactions
	def send_transaction(self):
		"""Sends a transaction to the connected node
		
		[description]
		"""
		pass

	def handel_transaction(self, new_transaction):
		"""what to do when a transaction is received
		
		when receiving the transaction, we verify it and add it the block

		:param new_transaction: the new transaction *{'information_type':'post_transaction','data':transaction}*
		:type new_transaction: str
		"""
		new_transaction = json.loads(new_transaction) # convert to json
		
		transaction = Transaction.json_to_transaction(new_transaction['data'])
		self.factory.blockchain.create_append_transaction(transaction)
		
		self._debug('Sending \'transaction_done\'')
		done_json = json.dumps({'information_type': 'transaction_done'})
		self.transport.write((done_json + '\n').encode())


	# Starting a client instance
	def connect_to(self, ip, port):
		"""This method connect to a node *'as a client'*
		
		[description]
		:param ip: id address
		:type ip: str
		:param port: port number
		:type port: int
		*@Override from ClientProtocol*
		"""
		def to_do(protocol):
			protocol.send_handshake()
			time.time(60)
			protocol.send_get_blockchain()

		connection_point = TCP4ClientEndpoint(reactor, ip, int(port))
		d = connectProtocol(connection_point, P2Protocol(self.factory,node_type=2))
		d.addCallback(to_do)

	def _debug(self, msg, pprint=False):
		"""Prints helpful information in debug mode
		
		_debug print with different color depending on the node_type 
		:param msg: the message to display
		:type msg: string
		:param pprint: prints a msg with a pprint *with indentation*, defaults to False
		:type pprint: bool, optional
		"""
		if self.debug:
			if not pprint:
				print(colored(msg,'red' if self.node_type == 1 else 'blue'))
			else:
				pp(msg, indent=4, width=4)
