"""	Client script, Run a ClientEndPoint 
and broadcast a transaction into the network
"""
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet import reactor
from modules.protocols.protocol_client import *


if __name__ == '__main__':
	print('--Start')
	host, port = "localhost", 5000

	seed_point = TCP4ClientEndpoint(reactor, host, port)
	connect = connectProtocol(seed_point, ClientProtocol())
	connect.addCallback(lambda p: p.send_handshake())
	reactor.run()
