#!/usr/bin/env python3

#By @pshem and @ZsanettM 2018, Licensed Apache 2.0
#tested in Python 3.5

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

#get the number of letters
numLetters = 0
for letter in important_chars:
	numLetters += letter_frequency[letter]

englishFrequency = dict(a=8.167, b=1.492, c=2.782, d=4.253, e=12.702, f=2.228,
 g=2.015, h=6.094, i=6.966, j=0.153, k=0.772, l=4.025, m=2.406, n=6.749,
  o=7.507, p=1.929, q=0.095, r=5.987, s=6.327, t=9.056, u=2.758, v=0.978,
   w=2.360, x=0.150, y=1.974, z=0.074)


fmt = "{letter:s}\t{FoundInText:d}\t{FrequencyInText:0.2f}%\t{FrequencyInEnglish:0.2f}%"
head = "{letter:s}\t{FoundInText:s}\t{FrequencyInText:s}\t{FrequencyInEnglish:s}"
#print('Letter \t','Times \t', '% of Text \t', '% of English')

print(head.format(letter = 'Letter', FoundInText = 'Times', FrequencyInText = 'Freq',FrequencyInEnglish = 'Freq'))
print(head.format(letter = '', FoundInText = 'in', FrequencyInText = 'in',FrequencyInEnglish = 'in'))
print(head.format(letter = '', FoundInText = 'text', FrequencyInText = 'text',FrequencyInEnglish = 'English'))

for letter in important_chars:
    print(fmt.format(letter = letter, FoundInText = letter_frequency[letter],
	 FrequencyInText = ((letter_frequency[letter]/numLetters)*100),
	 FrequencyInEnglish = englishFrequency[letter])) #if english letters
