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
elif len(sys.argv) == 3:
	if (sys.argv[2] != '-c'):
		raise ValueError('Use -c if you want case insensitive parsing')

ciphertext = []

#select the characters you want to deal with
important_chars = string.ascii_lowercase + string.ascii_uppercase

with open(sys.argv[1], 'r') as encryptedFile:
	for line in encryptedFile:
		#remove trailing newlines
		while line.endswith(chr(10)): #'/n' newline
			if (sys.argv[2] == '-c'):
				line = line[:-1].lower()
				important_chars = string.ascii_lowercase
			else:
				line = line[:-1]
		ciphertext.append(line)
		print(ciphertext[-1])

letter_frequency = collections.Counter()

for i in ciphertext:
	freq = collections.Counter(i)
	letter_frequency += freq

#print(letter_frequency) #would also print characters we don't want



for letter in important_chars:
    print(letter, " : ", letter_frequency[letter])
