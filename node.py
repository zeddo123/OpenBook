"""Node script: Runs a ServerEndPoint to access the network
"""
if __name__ == '__main__':
	from modules.factory_node import *

	port = int(input('port -> '))

	endpoint = TCP4ServerEndpoint(reactor, port)

	node_factory = P2PFactory(port)
	endpoint.listen(node_factory)

	reactor.run()

