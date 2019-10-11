"""	Seed Server script,
	Has the role of a "DNS" or "Track server",
	links new nodes to the network
"""
from modules.factory_seeds import *

endpoint = TCP4ServerEndpoint(reactor, 5989)
endpoint.listen(SeedFactory())
print('[Seeds Server is Up]')
reactor.run()