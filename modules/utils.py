from uuid import uuid4
import argparse

"""Funcion that generate a
universally unique identifier"""
uuid_generator = lambda: str(uuid4())

def max_pow_2(number_peers):
	"""Return the powers of 2 >= to the number of peers"""
	powers = []
	x = 0
	while 2**x < number_peers:
		powers.append(2**x)
		x += 1
	return powers + [2**x]

def argparser(description):
	"""Create a parser for the argument
	
	make a parser with the appropriate options *port number*, *debug mode* 
	
	:param description: description of the script *example: node description*
	:type description: str

	:returns: argparse for the script
	:type return: argparse object
	"""
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('-p', '--port', metavar='N', type=int, help='the port number', required=True)
	parser.add_argument('-d', '--debug', help='Activate the debug mode aka verbose', action='store_true')
	
	return parser
