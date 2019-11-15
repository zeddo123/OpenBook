"""	Seed Server script,
	Has the role of a "DNS" or "Track server",
	links new nodes to the network
"""

if __name__ == '__main__':
	from modules.factories.factory_seeds import *
	from modules.utils import argparser

	parser = argparser(description='Seed Server script,Has the role of a "DNS" or "Track server",links new nodes to the network')
	
	arg = parser.parse_args()
	port = int(arg.port)
	#port = 5989 # for the development
	
	if arg.debug:
		print('[Seeds Server is Up]')
	
	endpoint = TCP4ServerEndpoint(reactor, port)
	endpoint.listen(SeedFactory())
	reactor.run()
