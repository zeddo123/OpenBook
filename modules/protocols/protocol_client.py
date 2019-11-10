# Imports from the twisted module
from twisted.internet.protocol import Protocol
from twisted.internet.task import LoopingCall
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet import reactor

# Import from standard modules
import sys
sys.path.insert(0, '..')

from modules.blockchain.transaction import Transaction
from modules.blockchain.book import Book 

from time import time
from operator import xor
import json
from pprint import pprint


class ClientProtocol(Protocol):
	"""
		the Client protocol
		
		:Attributes:
			:attr debug: debug mode, *default to **True***
			:type debug: bool
		:Methods:
			:Twisted specific:
				:meth connectionMade: triggered when the connection is made
				:meth connectionLost: triggered when the connection is lost
				:meth dataReceived: every time a data is received, this method is called
			:Handling Initialisation:
				:meth send_ping: Send a ping request
				:meth send_pong: Respond with a pong
				:meth handel_pong: called when a pong is received
				:meth send_handshake: Send all the informations about the node
			:Getting new peers:
				:meth handel_post_peers: called when new peers are received
			:Starting a client instance:
				:meth connect_to: This method connect to a node *'as a client'*
	"""
	def __init__(self):
		Protocol.__init__(self)
		self.debug = True

	def connectionMade(self):
		self._debug(f'Connection Made with {self.transport.getPeer()}')


	def connectionLost(self, reason):
		self._debug(f'Connection Lost')


	def dataReceived(self, data):
		self._debug(f'---------------Received Data---------------')

		for line in data.decode('utf-8').splitlines():
			line = line.strip()
			current_data = json.loads(line)
			info_type = current_data['information_type']
			pprint(current_data,indent=4,width=4)

			if info_type == 'handshake':
				self.state = 'Active'
			
			elif info_type == 'ping':
				self.send_pong()
			elif info_type == 'pong':
				self.handel_pong(line)
			
			elif info_type == 'post_peers':
				self.handel_post_peers(line)

			elif info_type == 'transaction_done':
				self.handel_done_transaction()

	# Send ping to the connected node
	def send_ping(self):
		"""Send ping to the connected node

		:var ping_json: stores the ping request which will be sent
		:type ping_json: json
		"""
		ping_json = json.dumps({'information_type': 'ping'})
		self._debug(f'Pinging {self.remote_nodeid}')
		self.transport.write((ping_json + '\n').encode())

	# Send pong to the connected node
	def send_pong(self):
		"""Send pong to the connected node
		
		:var ping_json: stores the pong request which will be sent
		:type ping_json: json
		"""
		pong_json = json.dumps({'information_type': 'pong'})
		self._debug(f'Ponging {self.remote_nodeid}')
		self.transport.write((pong_json + '\n').encode())


	def handel_pong(self, pong):
		self._debug(f'Node {self.remote_nodeid} still active ::{pong}')


	def send_handshake(self):
		"""Sends a handshake to the new connection
		
		:var hs: contains the handshake request with all the information concerning the client
			* information_type
			* id 
			* ip of the client
			* port of the client
		:type hs: json
		"""
		self._debug(f'Sending handshake {self.transport.getPeer()}')
		hs = json.dumps({
						'information_type': 'handshake',
						'nodeid': 'client',
						'my_ip': '',
						'my_port': ''
						})
		self.transport.write((hs+'\n').encode())

	def handel_post_peers(self, peers):
		self._debug(':: Post peers Received')
		peers = json.loads(peers)
		number_queue = peers['number_queue']
		self.remote_nodeid = peers['nodeid']

		for rank, peer in peers['known_peers'].items():
			peer = peer.split(':')
			ip = peer[1]
			port = peer[2]
			print(ip,port)
			status = self.connect_to(ip,port)
			if status:
				break
		self.transport.loseConnection()

	def send_transaction(self):
		sender = input('sender -> ')
		title = input('title -> ')
		author = input('author -> ')
		date = input('date ->')
		genre = input('genre ->')

		book = Book(title,author,date,genre)
		trans = Transaction(sender,None,book)
		try:
			byte_trans = json.dumps({'information_type':'post_transaction','data':trans.to_json()})
			self.transport.write((byte_trans+'\n').encode())

		except Exception as e:
			self._debug('Exception occurred (dumping and sending the data)')
		else:
			self._debug(':: Transaction sent ::')

	def handel_done_transaction(self):
		self.transport.loseConnection()

	def connect_to(self, ip, port):
		try:
			connection_point = TCP4ClientEndpoint(reactor, ip, int(port))
			d = connectProtocol(connection_point, ClientProtocol())
			d.addCallback(lambda p: p.send_transaction())
			return True
		except:
			return False

	def _debug(self, msg):
		"""Prints helpful information in debug mode
		
		:param msg: the message to display
		:type msg: string
		"""
		if self.debug: print(msg)