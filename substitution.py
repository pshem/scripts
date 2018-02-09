#!/usr/bin/env python3
#

import sys
import string

#if !sys.argv[1]:


#encryptedFile = open(, 'r')

with open(sys.argv[1], 'r') as encryptedFile:
	#ciphertext = encryptedFile.read()
	for line in encryptedFile:
		print(line, end='')


print(type(encryptedFile), type(ciphertext))

#encryptedFile.close()
