#!/usr/bin/env python3
#

import sys
import string

if len(sys.argv) == 0:
	raise ValueError('No file to decode passed')
elif len(sys.argv) > 1:
	raise ValueError('Too many arguments passed. Pass just one')


#encryptedFile = open(, 'r')

with open(sys.argv[1], 'r') as encryptedFile:
	#ciphertext = encryptedFile.read()
	for line in encryptedFile:
		print(line, end='')


print(type(encryptedFile), type(ciphertext))

#encryptedFile.close()
