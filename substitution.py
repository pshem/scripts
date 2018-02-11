#!/usr/bin/env python3

#By @pshem and @ZsanettM 2018, Licensed Apache 2.0
#tested in Python 3.5

import sys
import string
import collections
import argparse

parser = argparse.ArgumentParser(description='This script will perform frequency analysis on the passed file')
parser.add_argument('infile', help="Pass the file you want to analyse")
case = parser.add_mutually_exclusive_group()
case.add_argument('-c', '--case-insensitive', action="store_true",
 dest="case", help="Pass if you want to ignore case", default=True)
case.add_argument('-C', '--case-sensitive', action='store_false',
 dest="case", help="Pass if you care about the case", default=True)
args = parser.parse_args()

ciphertext = []

#select the characters you want to deal with. Others will not be altered
important_chars = string.ascii_lowercase + string.ascii_uppercase

print(type(args.infile))

#read the file into a list of strings(1 string per line)
with open(args.infile, 'r') as encryptedFile:
	for line in encryptedFile:
		#remove trailing newline(s)
		while line.endswith(chr(10)): #'/n' newline
			line = line[:-1]

		#if case insensitive mode is turned on, turn all chars lowercase
		if args.case:
			line = line.lower()
			important_chars = string.ascii_lowercase

		ciphertext.append(line)
		#print the newly appended line
		print(ciphertext[-1])

#get the frequency at which particular letters are present in text
letter_freq = collections.Counter()
for i in ciphertext:
	freq = collections.Counter(i)
	letter_freq += freq

#get all letters which appear next to themselves, like 'm' in common
di_letter_freq = collections.Counter()
#for i in ciphertext:
#TODO: Implement


word_freq = collections.Counter()
for i in ciphertext:
	#divide on whitespace
	words = i.split()
	freq = collections.Counter(words)
	word_freq += freq

#get the total number of letters
numLetters = 0
for letter in important_chars:
	numLetters += letter_freq[letter]

#statistics from https://en.wikipedia.org/wiki/Letter_frequency
englishFrequency = collections.defaultdict(lambda:0, a=8.167, b=1.492, c=2.782,
 d=4.253, e=12.702, f=2.228, g=2.015, h=6.094, i=6.966, j=0.153, k=0.772,
 l=4.025, m=2.406, n=6.749, o=7.507, p=1.929, q=0.095, r=5.987, s=6.327,
 t=9.056, u=2.758, v=0.978, w=2.360, x=0.150, y=1.974, z=0.074)

#format the frequency table roughly with tabs
#TODO:redo with https://docs.python.org/3.5/library/string.html#format-specification-mini-language
head = "{a:s}\t{b:s}\t{c:s}\t{d:s}"
fmt = "{a:s}\t{b:d}\t{c:0.2f}%\t{d:0.2f}%"

print(head.format(a = 'Letter', b = 'Times', c = 'Freq', d = 'Freq'))
print(head.format(a = '', b = 'in', c = 'in', d = 'in'))
print(head.format(a = '', b = 'text', c = 'text', d = 'English'))

for letter in important_chars:
    print(fmt.format(a = letter, b = letter_freq[letter],
	 c = ((letter_freq[letter]/numLetters)*100),
	 d = englishFrequency[letter])) #if english letters

#word frequency table
#TODO: strip the '-' word
unique_words = word_freq.most_common()		#turn the Counter into a list
one_letter_word_freq = list()				#create separate lists for one,
two_letter_word_freq = list()				#two and three letter words
tri_letter_word_freq = list()				#and longer ones, but only if they
long_word_freq = list()						#appear multiple times
#<list>[x][0] gives the key, <list>[x][1] gives the number
numWords = len(unique_words) #may containg junk such as -

for i in unique_words:
	#print(i[0], i[1])	#for debugging
	if len(i[0]) == 1:
		one_letter_word_freq.append(i)
	elif len(i[0]) == 2:
		two_letter_word_freq.append(i)
	elif len(i[0]) == 3:
		tri_letter_word_freq.append(i)
	elif i[1] > 1:
		long_word_freq.append(i)
print()
print(head.format(a = 'Word', b = 'Times', c = 'Freq', d = 'Freq'))
print(head.format(a = '', b = 'in', c = 'in', d = 'in'))
print(head.format(a = '', b = 'text', c = 'text', d = 'English'))
for i in one_letter_word_freq:
    print(fmt.format(a = i[0], b = i[1], c = ((i[1]/numWords)*100), d = 0))
for i in two_letter_word_freq:
    print(fmt.format(a = i[0], b = i[1], c = ((i[1]/numWords)*100), d = 0))
for i in tri_letter_word_freq:
    print(fmt.format(a = i[0], b = i[1], c = ((i[1]/numWords)*100), d = 0))
for i in long_word_freq:
    print(fmt.format(a = i[0], b = i[1], c = ((i[1]/numWords)*100), d = 0))
