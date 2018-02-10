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

#select the characters you want to deal with. Others will not be altered
important_chars = string.ascii_lowercase + string.ascii_uppercase

#read the file into a list of strings(1 string per line)
with open(sys.argv[1], 'r') as encryptedFile:
	for line in encryptedFile:
		#remove trailing newline(s)
		while line.endswith(chr(10)): #'/n' newline
			line = line[:-1]

		#if case insensitive mode is turned on, turn all chars lowercase
		if (sys.argv[2] == '-c'):
			line = line.lower()
			important_chars = string.ascii_lowercase

		ciphertext.append(line)
		#print the newly appended line
		print(ciphertext[-1])

#get the frequency at which particular letters are present in text
letter_frequency = collections.Counter()
for i in ciphertext:
	freq = collections.Counter(i)
	letter_frequency += freq

#get the total number of letters
numLetters = 0
for letter in important_chars:
	numLetters += letter_frequency[letter]

#statistics from https://en.wikipedia.org/wiki/Letter_frequency
englishFrequency = dict(a=8.167, b=1.492, c=2.782, d=4.253, e=12.702, f=2.228,
 g=2.015, h=6.094, i=6.966, j=0.153, k=0.772, l=4.025, m=2.406, n=6.749,
  o=7.507, p=1.929, q=0.095, r=5.987, s=6.327, t=9.056, u=2.758, v=0.978,
   w=2.360, x=0.150, y=1.974, z=0.074)

#format the frequency table roughly with tabs
#TODO:redo with https://docs.python.org/3.5/library/string.html#format-specification-mini-language
head = "{letter:s}\t{TimesInText:s}\t{OddsInText:s}\t{OddsInEnglish:s}"
fmt = "{letter:s}\t{TimesInText:d}\t{OddsInText:0.2f}%\t{OddsInEnglish:0.2f}%"

print(head.format(letter = 'Letter', TimesInText = 'Times', OddsInText = 'Freq', OddsInEnglish = 'Freq'))
print(head.format(letter = '', TimesInText = 'in', OddsInText = 'in', OddsInEnglish = 'in'))
print(head.format(letter = '', TimesInText = 'text', OddsInText = 'text', OddsInEnglish = 'English'))

for letter in important_chars:
    print(fmt.format(letter = letter, TimesInText = letter_frequency[letter],
	 OddsInText = ((letter_frequency[letter]/numLetters)*100),
	 OddsInEnglish = englishFrequency[letter])) #if english letters
