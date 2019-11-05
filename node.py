"""Node script: Runs a ServerEndPoint to access the network
"""
if __name__ == '__main__':
	from modules.utils import argparser
	from modules.factories.factory_node import *

	parser = argparser(description='Runs a ServerEndPoint to access the network')
	
	arg = parser.parse_args()
	port = int(arg.port)

	if arg.debug:
		print(17 * '_' + 'Start' + 17 * '_')

	endpoint = TCP4ServerEndpoint(reactor, port)

	node_factory = P2PFactory(port)
	endpoint.listen(node_factory)

	reactor.run()

