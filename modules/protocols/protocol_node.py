# Imports from the twisted module
from twisted.internet.protocol import Protocol
from twisted.internet.task import LoopingCall
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet import reactor

# Import from standard modules
from time import time
from operator import xor
import json

# Import from custom modules
import sys
sys.path.insert(0, '..')

from modules.utils import max_pow_2
from modules.blockchain.transaction import Transaction


class P2Protocol(Protocol):
	"""
		docstring for the peer-2-peer protocol
		
		:attr node_type:

		1. Server instance of P2Protocol
		2. client instance of P2Protocol
		
		:type node_type: int
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


	def connectionMade(self):
		self.factory._debug(f'{ "<-" if self.node_type == 1 else "->" }Connection Made with {self.transport.getPeer()}', self.node_type)
		self.my_ip = self.transport.getHost().host

	def connectionLost(self, reason):
		self.factory._debug(f'Connection Lost with {self.remote_nodeid} {reason}', self.node_type)
		if self.remote_nodeid in self.factory.known_peers:
			self.factory.known_peers.pop(self.remote_nodeid)
			if self.loop_ping.running == True:
				self.loop_ping.stop()


	def dataReceived(self, data):
		self.factory._debug(f'---------------Received Data---------------', self.node_type)
		
		for line in data.decode('utf-8').splitlines():
			
			line = line.strip()
			current_data = json.loads(line)
			self.factory._debug(current_data,self.node_type,pprint=True)

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

		self.factory._debug('__________________________________________\n\n\n\n', self.node_type)

	# Handling Initialisation
	def send_ping(self):
		"""Send ping to the connected node

		:var ping_json: stores the ping request which will be sent
		:type ping_json: json
		"""
		ping_json = json.dumps({'information_type': 'ping'})
		self.factory._debug(f'Pinging {self.remote_nodeid}', self.node_type)
		self.transport.write((ping_json + '\n').encode())

	def send_pong(self):
		"""Send pong to the connected node
		
		:var ping_json: stores the pong request which will be sent
		:type ping_json: json
		"""
		pong_json = json.dumps({'information_type': 'pong'})
		self.factory._debug(f'Ponging {self.remote_nodeid}',self.node_type)
		self.transport.write((pong_json + '\n').encode())

	def handel_pong(self, pong):
		"""when receiving a pong we are sure that the node is alive
		
		we print a msg (in debug mode) notifing that the node is alive
		and we save the time at which the pong was received

		:param pong: the msg received
		:type pong: str
		"""
		self.factory._debug(f'Node {self.remote_nodeid} still active ::{pong}', self.node_type)
		self.last_ping = time()

	def send_handshake(self):
		"""Sends a handshake to the new connection
		
		:var hs: contains the handshake request with all the information concerning the node
		
			* information_type
			* nodeid
			* ip of the node
			* port of the node

		:type hs: json
		"""
		self.factory._debug(f'Sending handshake {self.transport.getPeer()}', self.node_type)
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
			self.factory._debug('Oups, Connected to myself')
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
				self.factory._debug('Looping Call started', self.node_type)
				self.loop_ping.start(60 * 5) # Start pinging every 5 mins

	# Getting new peers
	def handel_post_peers(self, peers):
		"""deals with what to 
		do when a new list of node is received
		
		loop through the peers and connect to them by following the kademlia routing table

		:param peers: list of new peers
		:type peers: json/dict
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
				self.factory._debug('Found New Node :: Connecting', self.node_type)
				self.connect_to(ip,port)


	# Sending/Posting/Handling the block-chain
	def send_get_blockchain(self):
		"""The method that sends a request to get a chain"""

		block_json = json.dumps({'information_type': 'get_blockchain'})
		self.factory._debug(f'Send get_blockchain request {self.remote_nodeid}', self.node_type)
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
			self.factory._debug('-> Updating Local Blockchain', self.node_type)
		else:
			self.factory._debug('-> Updating Local Blockchain -> Local Blockchain longer', self.node_type)


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
		
		self.factory._debug('Sending \'transaction_done\'', self.node_type)
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
		"""
		def to_do(protocol):
			protocol.send_handshake()
			time.time(60)
			protocol.send_get_blockchain()

		connection_point = TCP4ClientEndpoint(reactor, ip, int(port))
		d = connectProtocol(connection_point, P2Protocol(self.factory,node_type=2))
		d.addCallback(to_do)
