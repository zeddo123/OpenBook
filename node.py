from modules.factory_node import *

port = int(input('port'))
endpoint = TCP4ServerEndpoint(reactor, port)
endpoint.listen(P2PFactory(port))
reactor.run()