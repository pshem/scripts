#!/usr/bin/env python3

#By @pshem and @ZsanettM 2018, Licensed Apache 2.0
#tested in Python 3.5

import sys
import string
import collections
import argparse
import json

def parseCiphertext(infile, case, verbose):
	ciphertext = []
	#read the file into a list of strings(1 string per line)
	with open(infile, 'r') as encryptedFile:
		for line in encryptedFile:
			#remove trailing newline(s)
			while line.endswith(chr(10)): #'/n' newline
				line = line[:-1]
			#if case insensitive mode is turned on, turn all chars lowercase
			if case:
				line = line.lower()
			ciphertext.append(line)
			if verbose:
				#print the newly appended line
				print(ciphertext[-1])
	return ciphertext
#end parseCiphertext

#TODO: performance optimisations
def getFrequencies(text, important_chars):
	letter_freq = collections.Counter()
	di_letter_freq = collections.Counter()
	word_freq = collections.Counter()

	#letter frequency table
	for i in text:
		#get the frequency at which letters are present in text
		freq = collections.Counter(i)
		letter_freq += freq
		#get all letters which appear next to themselves, like 'm' in common
		for j, k in zip(i, i[1:]):
			if j == k and j in important_chars:
				di_letter_freq[j] +=1
		#divide on whitespace
		words = i.split()
		freq = collections.Counter(words)
		word_freq += freq

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
	return list([letter_freq, di_letter_freq, one_letter_word_freq, two_letter_word_freq, tri_letter_word_freq, long_word_freq, numWords])
#end getFrequencies()

# TODO: roll into getFrequencies()
# get the total number of letters
def countLetters(letter_freq, important_chars):
	numLetters = 0
	for letter in important_chars:
		numLetters += letter_freq[letter]
	return numLetters

def json2python(j):
	letterFreq = collections.defaultdict(lambda:  0)
	letterFreq.update(j["letterFreq"]["data"])
	diLetterList = frozenset(j["diLetterList"]["data"])
	wordList = list()
	wordList.append("")
	wordList.append(frozenset(j["wordList"]["data"]["1"]))
	wordList.append(frozenset(j["wordList"]["data"]["2"]))
	wordList.append(frozenset(j["wordList"]["data"]["3"]))
	wordList.append(frozenset(j["wordList"]["data"]["4"]))
	return list([letterFreq, diLetterList, wordList[1], wordList[2], wordList[3], wordList[4]])
#end json2python(j)

# compare text with average English.  The lower, the better
def howEnglish(text, important_chars, lang):
	quantities = getFrequencies(text, important_chars)
	numLetters = countLetters(quantities[0], important_chars)
	#TODO: scale expected divergence with length of text
	expected_error = 3
	score = 0

# punish large differences in letter frequency
	for letter in important_chars:
# add 0 if the error is smaller than expected error
		score += max(0, abs((quantities[0][letter]/numLetters)*100 - lang[0][letter]) - expected_error)
		#print(letter + " " + str(score)) #for debugging
# punish diletters not present in English
# TODO: special case with too many different diletters?
	for i in quantities[1]:
		#add 3 for each diletter not present in English. Possible problem with SPACELESSTEXT
		score += 3 * (not bool(str(i[0]+i[0]) in lang[1]))
		#print(i[0] + i[0] + " " + str(score)) #for debugging
# reward presence of well known words
	for i in quantities[2]:	# TODO: allow lowercase i in case insensitive mode(-c)
		score -= bool(i[0] in lang[2])
	for i in quantities[3]:
		score -= bool(i[0] in lang[3])
	for i in quantities[4]:
		score -= bool(i[0] in lang[4])
	for i in quantities[5]:
		score -= bool(i[0] in lang[5])
	return score
#end howEnglish()

def cesarShift(encrypted, rot, rotatingSurface):
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
	while ord(result[-1]) == 10: #'/n' newline
		result = result[:-1]
	return result
#end cesarShift()

def bestCesarShift(ciphertext, important_chars, lang):
	lowest_score = 100;
	shift = 0;
	for i, j in enumerate(important_chars):
		text = cesarShift(ciphertext, i, important_chars)
		score = howEnglish(text, important_chars, lang)
		lowest_score = min(lowest_score, score)
		if lowest_score == score:
			shift = i
	return shift
# end bestCesarShift()

def printStatistics(text, important_chars, lang):

	quantities = getFrequencies(text, important_chars)
	numLetters = countLetters(quantities[0], important_chars)

	#format the frequency table roughly with tabs
	#TODO:redo with https://docs.python.org/3.5/library/string.html#format-specification-mini-language
	head = "{a:s}\t{b:s}\t{c:s}\t{d:s}"
	head2 = "{a:s}\t{b:s}\t{c:s}\t{d:s}\t\t{e:s}\t{f:s}\t{g:s}"
	fmt = "{a:s}\t{b:d}\t{c:0.2f}%\t{d:0.2f}%"
	fmt2 = "{a:s}\t{b:d}\t{c:0.2f}%\t{d:0.2f}%\t\t{e:s}\t{f:d}\t{g:b}"

	print(head2.format(a = 'Letter', b = 'Times', c = 'Freq', d = 'Freq', e = 'Letter', f = 'Is', g = 'Is'))
	print(head2.format(a = '', b = 'in', c = 'in', d = 'in', e = "Sequ-", f = 'in', g = 'in'))
	print(head2.format(a = '', b = 'text', c = 'text', d = 'English', e = 'ence', f = 'Text', g = 'English'))

	for letter in important_chars:
		print(fmt2.format(a = letter, b = quantities[0][letter],
		 c = (quantities[0][letter]/numLetters)*100,
		 d = lang[0][letter], e = letter+letter, f = bool(quantities[1][letter]),
		 g = bool(letter+letter in lang[1]))) #if english letters

	print()
	print(head.format(a = 'Word', b = 'Times', c = 'Freq', d = 'Freq'))
	print(head.format(a = '', b = 'in', c = 'in', d = 'in'))
	print(head.format(a = '', b = 'text', c = 'text', d = 'English'))
	for i in quantities[2]:
		print(fmt.format(a = i[0], b = i[1], c = ((i[1]/quantities[6])*100), d = 0))
	for i in quantities[3]:
		print(fmt.format(a = i[0], b = i[1], c = ((i[1]/quantities[6])*100), d = 0))
	for i in quantities[4]:
		print(fmt.format(a = i[0], b = i[1], c = ((i[1]/quantities[6])*100), d = 0))
	for i in quantities[5]:
		print(fmt.format(a = i[0], b = i[1], c = ((i[1]/quantities[6])*100), d = 0))
	print("Score: " + str(howEnglish(text, important_chars, lang)))

def main(argv=None):
	if argv is None:
		argv = sys.argv

	#parse command-line arguments
	parser = argparse.ArgumentParser(description='This script will perform frequency analysis on the passed file')
	parser.add_argument('infile', help="Pass the file you want to analyse")
	case = parser.add_mutually_exclusive_group()
	case.add_argument('-c', '--case-insensitive', action="store_true",
	dest="case", help="Pass if you want to ignore case(default)", default=True)
	case.add_argument('-C', '--case-sensitive', action='store_false',
	dest="case", help="Pass if you care about the case", default=True)
	parser.add_argument('-l', '--lang', default="lang/english.json",
	help="Pass the path to a language statistics file", type=argparse.FileType('r', encoding='UTF-8'))
	parser.add_argument('-v', '--verbose', action="count",
	help="Pass once to print the ciphertext. To be extended")
	args = parser.parse_args()

	# load english frequencies from json
	lang = json2python(json.load(args.lang))

	#letterFreq = lang[0]
	#diLetterList = lang[1]
	#wordList1 = lang[2]
	#wordList2 = lang[3]
	#wordList3 = lang[4]
	#wordList4 = lang[5]

	if args.case:
		important_chars = string.ascii_lowercase
	else:
		important_chars = string.ascii_lowercase + string.ascii_uppercase

	# get the ciphertext out of the file
	ciphertext = parseCiphertext(args.infile, args.case, args.verbose)

	# analyse original text
	quantities = getFrequencies(ciphertext, important_chars)

	# count how many characters to work with
	numLetters = countLetters(quantities[0], important_chars)

	# decode the ciphertext
	plaintext = cesarShift(ciphertext, bestCesarShift(ciphertext, important_chars, lang), important_chars)

	printStatistics(plaintext, important_chars, lang)

	print(getFrequencies(plaintext, important_chars))
#end main(argv)

#based on https://www.artima.com/weblogs/viewpost.jsp?thread=4829
if __name__ == "__main__":
	sys.exit(main())
