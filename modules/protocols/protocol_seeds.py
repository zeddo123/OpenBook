from twisted.internet.task import LoopingCall

from time import time
import json

from modules.protocols.protocol_client import ClientProtocol

class SeedProtocol(ClientProtocol):
	"""SeedProtocol-the protocol that the seed server will follow
	
	:Attributes:
		:attr state: the state of the protocol instance *("waiting" or "active")*
		:type state: string

		:attr factory: the node-factory object for interacting with global variables
		:type factory: Factory -*Twisted*

		:attr remote_nodeid: the *uuid* of the connected-to node
		:type remote_nodeid: string

		:attr remote_ip: the ip address of the remote node
		:type remote_ip: string

		:attr loop_ping: a loopingCall to start pinging every 5 minutes
		:type loop_ping: LoopingCall -*twisted.internet.task*

		:attr last_ping: Last time the node sent a ping
		:type last_ping: int
	:Methods:
		:Twisted specific:
			:connectionLost: triggered when the connection is made -**Override from ClientProtocol**
			:dataReceived: triggered when the connection is lost -**Override from ClientProtocol**
		:Seed-Sever specific:
			:format_peers: create a list of all the known nodes with their ip, port and number in the queue 
				-*{'number_queue' : nodeis:ip:port}*
			:send_peers: Send all the known nodes to the new node.
			:_handel_node: Called when a new node connect to the seed server.
		:Handling Initialisation:
			:handel_pong: called when a pong is received.
			:handel_handshake: called when a handshake is received.
	"""
	def __init__(self, factory):
		self.state = 'waiting'
		self.factory = factory

		#Connected Node
		self.remote_nodeid = None
		self.remote_ip = None
		self.remote_port = None
		
		#Looping call to ping the connected nodes
		self.loop_ping = LoopingCall(self.send_ping) 
		self.last_ping = None

		ClientProtocol.__init__(self)

	def connectionLost(self, reason):
		self._debug(f'Connection Lost with {self.remote_nodeid}')
		
		if self.remote_nodeid != 'client':
			id_rank = self.remote_nodeid+':'+self.number_queue
			if  id_rank in self.factory.known_peers:
				self.factory.known_peers.pop(id_rank)
				self.loop_ping.stop()


	def dataReceived(self, data):

		self._debug(f'---------------Received Data---------------')
		
		for line in data.decode('utf-8').splitlines():
			line = line.strip()
			
			current_data = json.loads(line)
			info_type = current_data['information_type']
			self._debug(current_data,True)

			if info_type == 'handshake' and self.state != 'Active':
				self.handel_handshake(line)
				self.state = 'Active'
			elif info_type == 'ping':
				self.send_pong()
			elif info_type == 'pong':
				self.handel_pong(line)
			elif info_type == 'get_peers':
				self.send_peers()


	def format_peers(self):
		"""Create a formated dict, that holds all the information about the nodes *{'number_queue' : nodeis:ip:port}*
		
		the dict formated to be easy to send in a json file
		:returns: dict/json containing all the known nodes
		:rtype: {dict}
		"""
		formated_peers = {}
		for idn, peer in self.factory.known_peers.items():
			if peer != self:
				formated_peers[idn.split(':')[1]] = peer.remote_nodeid + ':' + peer.remote_ip + ':' + str(peer.remote_port)
		return formated_peers

	def handel_pong(self, pong):
		"""called when a pong is received
		
		when a pong is received, we can be sure about the state of the connected node
		:param pong: the pong msg
		:type pong: str
		"""
		self._debug(f'Node {self.remote_nodeid} still active ::{pong}')
		self.last_ping = time()

	def send_peers(self):
		"""Send all the known nodes.
		
		the send_peers msg will contain all the information about the seed server and his nodes::

		``
		{
			'information_type': 'post_peers',
			'nodeid': 'SeedServer',
			'number_queue': x,
			'known_peers': list of all node,
		}
		``
		"""
		self._debug(f'Sending Peers {self.transport.getPeer()}')
		hs = json.dumps({
						'information_type': 'post_peers',
						'nodeid': 'SeedServer',
						'number_queue': self.number_queue if self.remote_nodeid != 'client' else 'UNKNOWN',
						'known_peers': self.format_peers(),
						})

		self.transport.write((hs+'\n').encode())

	def handel_handshake(self, hs):
		"""called when a handshake is received.
		
		the handshake is either received from a client or a node
		for a client: we simply send a list of all the nodes
		for a node: first we add the node in the register and send back the list of the nodes 
		:param hs: the handshake data
		:type hs: string
		"""
		hs = json.loads(hs)
		
		#Extraction remote node information
		self.remote_nodeid = hs['nodeid']
		self.remote_ip = hs['my_ip']
		self.remote_port = hs['my_port']

		if hs['nodeid'] == 'client':
			self._debug('Received handshake from client :: Proceed sending nodes')
			self.send_peers()
		else:
			self._debug('Received handshake from node :: Proceed by adding to the list')
			self._handel_node(hs)

	def _handel_node(self, hs):
		"""Called when a new node connect to the seed server.
		"""
		self.number_queue = str(len(self.factory.known_peers))
		self.factory.known_peers[self.remote_nodeid+':'+ self.number_queue] = self
		self.send_peers()
		if self.loop_ping.running == False:
			self._debug('Looping ping call started')
			self.loop_ping.start(60 * 5) # Start pinging every 5min
