from twisted.internet.protocol import Protocol

class P2Protocol(Protocol):
	"""docstring for the peer-2-peer protocol"""
	def __init__(self, factory):
		self.factory = factory


	def connectionMade(self):
		self.factory.numProtocols += 1
		self.trasport.write('In the face of ambiguity refuse the temptation to guess')


	def connectionLost(self):
		print('Connection Lost')


	def dataReceived(self, data):
		print(data)