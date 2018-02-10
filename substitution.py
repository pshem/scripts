#!/usr/bin/env python3
#

import sys
import string
import collections

#check the number of arguments passed
if len(sys.argv) == 1:
	raise ValueError('No file passed to decode')
elif len(sys.argv) > 3:
	raise ValueError('Too many arguments passed. Pass just one')
elif len(sys.argv) == 2:
	if sys.argv[2] == '-c':
		#case insensitive
	else:
		raise ValueError('Use -c if you want case insensitive parsing')

ciphertext = []

with open(sys.argv[1], 'r') as encryptedFile:
	for line in encryptedFile:
		#remove trailing newlines
		while line.endswith(chr(10)): #'/n' newline
			line = line[:-1]
		ciphertext.append(line)
		print(ciphertext[-1])

letter_frequency = collections.Counter()

for i in ciphertext:
	freq = collections.Counter(i)
	letter_frequency += freq

#print(letter_frequency) #would also print characters we don't want

#select the characters you want to deal with
important_chars = string.ascii_lowercase + string.ascii_uppercase

for letter in important_chars:
    print(letter, " : ", letter_frequency[letter])
