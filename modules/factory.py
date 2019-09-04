from twisted.internet.protocol import Factory
from protocol import *

# Funcion that generate a
# universally unique identifier
uuid_generator = lambda: str(uuid4())

class P2PFactory(Factory):
	"""docstring for P2PFactory"""
	def __init__(self, max_peers, server_port, server_host=None, debug=True):
		# debug variable if True prints log in the terminal
		self.debug = debug
		# active variable, if True the peer is still running
		self.active = True

		# max_peers is the number of peers the peers can handel
		self.max_peers = max_peers
		self.server_port = server_port

		if serverhost:
			self.server_host = server_host
		else:
			self._init_server_host()

		self.uuid = uuid_generator()
		self.known_peers = {}

	def buildProtocol(self, addr):
		return P2Protocol()