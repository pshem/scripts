#!/usr/bin/env python3

#By @pshem and @ZsanettM 2018, Licensed: Apache2.0
#tested in Python 3.5

import sys
import string

#check the number of arguments passed
if len(sys.argv) == 1:
	raise ValueError('No file passed to decode')
elif len(sys.argv) > 2:
	raise ValueError('Too many arguments passed. Pass just one')

lowerUpper = string.ascii_lowercase + string.ascii_uppercase #+ string.digits

def decode(encrypted, rot, rotatingSurface):
	result = ""
	for i in range(len(encrypted)):
		if encrypted[i] in rotatingSurface:
			for j in range(len(rotatingSurface)):
				if encrypted[i] == rotatingSurface[j]:
					result += rotatingSurface[(j + rot) % len(rotatingSurface)]
		else:
			#don't change characters outside the rotatingSurface
			result += encrypted[i]
	#remove trailing newlines
	while ord(result[-1]) == 10: #'/n' neline
		result = result[:-1]
	return result

oldCiphertext = []

with open('decryptMe1.txt', 'r') as encryptedFile:
	for line in encryptedFile:
		oldCiphertext.append(line)

def test():
	test1 = decode(oldCiphertext[0], 45, lowerUpper)
	if (test1) == "Hence! home, you idle creatures get you home:":
		#print("Decoding works")
		return True
	else:
		print(test1, "Hence! home, you idle creatures get you home:")
		print(len(test1), len("Hence! home, you idle creatures get you home:"))
		raise ValueError('Something is wrong with decode')
		return False

#if self test works, then start decoding the given file
if test():
	ciphertext = []

	with open(sys.argv[1], 'r') as encryptedFile:
		for line in encryptedFile:
			ciphertext.append(line)

	print("ROT             Decoded string" )
	for b in range(len(lowerUpper)):
		if (b < 10): #for even positioning
			print("", b, " ", decode(ciphertext[0], b, lowerUpper))
		else:
			print(b, " ", decode(ciphertext[0], b, lowerUpper))
