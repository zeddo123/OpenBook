from uuid import uuid4

# Funcion that generate a
# universally unique identifier
uuid_generator = lambda: str(uuid4())

def max_pow_2(number_peers):
	# Return the powers of 2 >= to the number of peers
	powers = []
	x = 0
	while 2**x < number_peers:
		powers.append(2**x)
		x += 1
	return powers + [2**x]