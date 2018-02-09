#!/usr/bin/env python

import sys
import string

ciphertext = []

with open(sys.argv[1], 'r') as encryptedFile:
	for line in encryptedFile:
		ciphertext.append(line)

lowerUpper = string.ascii_lowercase + string.ascii_uppercase #+ string.digits

def decode(encrypted, rot, rotatingSurface):
	result = ""
	for i in range(len(encrypted)):
		if encrypted[i] in rotatingSurface:
			for j in range(len(rotatingSurface)):
				if encrypted[i] == rotatingSurface[j]:
					result += rotatingSurface[(j + rot) % len(rotatingSurface)]
					#result = rotatingSurface[len(rotatingSurface) - i]
		else:
			#don't change
			result += encrypted[i]
	return result

oldCiphertext = []

with open('decryptMe1.txt', 'r') as encryptedFile:
	for line in encryptedFile:
		oldCiphertext.append(line)

def test():
	if decode(oldCiphertext[0], 45, lowerUpper) is "Hence! home, you idle creatures get you home:":
		print("Decoding works")
		return true
	else:
		print(decode(oldCiphertext[0], 45, lowerUpper))
		raise ValueError('Something is wrong with decode')
		return false
test()
"""
for b in range(len(lowerUpper)):
	print(b, " ", decode(oldCiphertext, b, lowerUpper))
"""
"""
	print()
else:
	#print("Your code broke again")
"""
