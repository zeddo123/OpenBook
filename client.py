from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet import reactor
from modules.protocol_client import *


import pickle

host, port = "localhost", 5989

seed_point = TCP4ClientEndpoint(reactor, host, 5989)
connect = connectProtocol(seed_point, ClientProtocol())
connect.addCallback(lambda p: p.send_handshake())
reactor.run()