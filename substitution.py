#!/usr/bin/env python3
#

import sys
import string

#check the number of arguments passed
if len(sys.argv) == 1:
	raise ValueError('No file passed to decode')
elif len(sys.argv) > 2:
	raise ValueError('Too many arguments passed. Pass just one')

ciphertext = []

with open(sys.argv[1], 'r') as encryptedFile:
	for line in encryptedFile:
		#remove trailing newlines
		while line.endswith(chr(10)): #'/n' newline
			line = line[:-1]
		ciphertext.append(line)
		print(ciphertext[-1])


print(type(encryptedFile), type(ciphertext))
