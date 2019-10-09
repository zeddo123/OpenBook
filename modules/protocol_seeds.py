from twisted.internet.protocol import Protocol
from twisted.internet.task import LoopingCall
from time import time
import json
from pprint import pprint


class SeedProtocol(Protocol):
	"""docstring for the peer-2-peer protocol"""
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


	def connectionMade(self):
		self.factory._debug(f'Connection Made with {self.transport.getPeer()}')


	def connectionLost(self, reason):
		self.factory._debug(f'Connection Lost with {self.remote_nodeid}')
		
		if self.remote_nodeid != 'client':
			id_rank = self.remote_nodeid+':'+self.number_queue
			if  id_rank in self.factory.known_peers:
				self.factory.known_peers.pop(id_rank)
				self.loop_ping.stop()


	def dataReceived(self, data):

		self.factory._debug(f'---------------Received Data---------------')
		
		for line in data.decode('utf-8').splitlines():
			line = line.strip()
			
			current_data = json.loads(line)
			info_type = current_data['information_type']
			pprint(current_data,indent=4,width=-1)

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
		formated_peers = {}
		for idn, peer in self.factory.known_peers.items():
			if peer != self:
				formated_peers[idn.split(':')[1]] = peer.remote_nodeid + ':' + peer.remote_ip + ':' + str(peer.remote_port)
		return formated_peers

	def send_ping(self):
		ping_json = json.dumps({'information_type': 'ping'})
		self.factory._debug(f'Pinging {self.remote_nodeid}')
		self.transport.write((ping_json + '\n').encode())


	def send_pong(self):
		pong_json = json.dumps({'information_type': 'pong'})
		self.factory._debug(f'Ponging {self.remote_nodeid}')
		self.transport.write((pong_json + '\n').encode())


	def handel_pong(self, pong):
		self.factory._debug(f'Node {self.remote_nodeid} still active ::{pong}')
		self.last_ping = time()


	def send_peers(self):
		self.factory._debug(f'Sending Peers {self.transport.getPeer()}')
		hs = json.dumps({
						'information_type': 'post_peers',
						'nodeid': 'SeedServer',
						'number_queue': self.number_queue if self.remote_nodeid != 'client' else 'UNKNOWN',
						'known_peers': self.format_peers(),
						})

		self.transport.write((hs+'\n').encode())


	def handel_handshake(self, hs):
		hs = json.loads(hs)
		
		#Extraction remote node information
		self.remote_nodeid = hs['nodeid']
		self.remote_ip = hs['my_ip']
		self.remote_port = hs['my_port']

		if hs['nodeid'] == 'client':
			self.factory._debug('Received handshake from client :: Proceed sending nodes')
			self.send_peers()
		else:
			self.factory._debug('Received handshake from node :: Proceed by adding to the list')
			self._handel_node(hs)

	def _handel_node(self, hs):
		self.number_queue = str(len(self.factory.known_peers))
		self.factory.known_peers[self.remote_nodeid+':'+ self.number_queue] = self
		self.send_peers()
		if self.loop_ping.running == False:
			self.factory._debug('Looping ping call started')
			self.loop_ping.start(60 * 5) # Start pinging every 5mins