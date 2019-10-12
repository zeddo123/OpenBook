# Imports from the twisted module
from twisted.internet.protocol import Protocol
from twisted.internet.task import LoopingCall
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet import reactor

# Import from standard modules
from time import time
from operator import xor
import json
from pprint import pprint

# Import from custom modules
import sys
sys.path.insert(0, '..')

from modules.utils import max_pow_2


class P2Protocol(Protocol):
	"""
		docstring for the peer-2-peer protocol
			node_type : 1 - Server instance of P2Protocol
						2 - client instance of P2Protocol
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
		self.factory._debug(f'Connection Made with {self.transport.getPeer()}')
		self.my_ip = self.transport.getHost().host

	def connectionLost(self, reason):
		self.factory._debug(f'Connection Lost with {self.remote_nodeid}')
		if self.remote_nodeid in self.factory.known_peers:
			self.factory.known_peers.pop(self.remote_nodeid)
			self.loop_ping.stop()


	def dataReceived(self, data):
		self.factory._debug(f'---------------Received Data---------------')
		
		for line in data.decode('utf-8').splitlines():
			
			line = line.strip()
			current_data = json.loads(line)
			pprint(current_data,indent=4,width=-1)
			info_type = current_data['information_type']

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
				pass

	# Send ping to the connected node
	def send_ping(self):
		ping_json = json.dumps({'information_type': 'ping'})
		self.factory._debug(f'Pinging {self.remote_nodeid}')
		self.transport.write((ping_json + '\n').encode())

	# Send pong to the connected node
	def send_pong(self):
		pong_json = json.dumps({'information_type': 'pong'})
		self.factory._debug(f'Ponging {self.remote_nodeid}')
		self.transport.write((pong_json + '\n').encode())


	def handel_pong(self, pong):
		self.factory._debug(f'Node {self.remote_nodeid} still active ::{pong}')
		self.last_ping = time()


	def send_handshake(self):
		self.factory._debug(f'Sending handshake {self.transport.getPeer()}')
		hs = json.dumps({
						'information_type': 'handshake',
						'nodeid': self.nodeid,
						'my_ip': self.my_ip,
						'my_port': self.my_port
						})
		self.transport.write((hs+'\n').encode())	


	def handel_handshake(self, hs):
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
			if self.node_type == 1:
				self.send_handshake()
				self.connect_to(ip=hs['my_ip'], port=hs['my_port'])

			if self.loop_ping.running == False:
				self.factory._debug('Looping Call started')
				self.loop_ping.start(60 * 5) # Start pinging every 5mins


	def handel_post_peers(self, peers):
		peers = json.loads(peers)
		number_queue = peers['number_queue']
		self.remote_nodeid = peers['nodeid']

		for rank, peer in peers['known_peers'].items():
			peer = peer.split(':')
			ip = peer[1]
			port = peer[2]
			
			# Creating A connection following Kademlia RT
			if xor(int(number_queue),int(rank)) in max_pow_2(len(peers['known_peers'])+1):
				self.factory._debug('Found New Node :: Connecting')
				self.connect_to(ip,port)


	def send_get_blockchain(self):
		ping_json = json.dumps({'information_type': 'get_blockchain'})
		self.factory._debug(f'Send get_blockchain request {self.remote_nodeid}')
		self.transport.write((ping_json + '\n').encode())

	def send_blockchain(self):
		serial_block = json.dumps({
									'information_type': 'post_blockchain',
									'blockchain': self.factory.blockchain.to_json()
								})
		self.transport.write(serial_block)


	def handel_blockchain(self, blockchain):
		blockchain = json.loads(blockchain)['blockchain']
		if blockchain.number_blocks() > self.factory.blockchain.number_blocks():
			self.factory = blockchain
			self.factory._debug('-> Updating Local Blockchain')
		else:
			self.factory._debug('-> Updating Local Blockchain -> Local Blockchain longer')

	def send_transaction(self):
		pass


	def handel_transaction(self):
		pass


	def connect_to(self, ip, port):
		def to_do(protocol):
			protocol.send_handshake()
			time.time(60)
			protocol.send_get_blockchain()

		connection_point = TCP4ClientEndpoint(reactor, ip, int(port))
		d = connectProtocol(connection_point, P2Protocol(self.factory,node_type=2))
		d.addCallback(to_do)