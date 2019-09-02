import socket
import select
from uuid import uuid4
import datetime
import traceback


# Funcion that generate a
# universally unique identifier
# for every peer in the network
uuid_generator = lambda: str(uuid4())

class Peer:
	"""docstring for Peer"""
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

	def _create_server_socket(self, port, backlog=5):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind(( '', port ))
		s.listen(backlog)
		return s

	@staticmethod
	def _debug(msg):
		if self.debug: print(msg)

	def listening(self):
		server_socket = _create_server_socket(self.server_port)
		server_socket.settimeout(2)

		timestamp = datetime.datetime.now().__str__()
		self._debug(f'Server started [{self.uuid}:{self.uuid}] at {timestamp}')

		while self.active:
			self._debug( 'Listening for connections...' )
			try:
				read_sock, _, exception_sock = select.select(socket_list, [], socket_list)
				for notified_sock in read_sock:
					if notified_sock == server_socket:
						# --New connection
						client_socket, client_address = server_socket.accept()
						client_socket.settimeout(None)
						self._debug(f'New connection accepted [{client_socket}:{client_address}]')
			
			except KeyboardInterrupt:
				self.active = False
			except:
				self._debug(traceback.print_exc())
				continue

		server_socket.close()
