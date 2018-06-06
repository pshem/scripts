#!/usr/bin/env python3

#By @pshem and @ZsanettM 2018, Licensed Apache 2.0
#tested in Python 3.5

"""Apply and break simple encryption algorithms

Module intended to save time on low point crypto
challenges in CTFs.
"""

import sys
import collections
import argparse
import json

def parse_ciphertext(infile, case, verbose):
    """Convert input file into a string

    Strip newlines and normalise to lowercase if -c is used.
    Print the whole string after every line if -v"""
    ciphertext = ""
    #read the file into a list of strings(1 string per line)
    for line in infile:
        #remove trailing newline(s)
        while line.endswith(chr(10)): #'/n' newline
            line = line[:-1] + " "
        #if case insensitive mode is turned on, turn all chars lowercase
        if case:
            line = line.lower()
        ciphertext += line
        if verbose:
            #print the newly appended line
            print(ciphertext)
    return ciphertext
#end parse_ciphertext

#TODO: performance optimisations
def get_frequencies(text, important_chars):
    """Analyze the text for character frequency and common words

    Returns an 8 element list of:
    1: character quantities
    2: double character("ee") quantities
    3: one character long word quantities
    4: two character long word quantities
    5: three character long word quantities
    6: longer word quantities
    7: total number of words
    8: total number of characters(present in "alphabet" in json)
    """
    letter_freq = collections.Counter()
    di_letter_freq = collections.Counter()
    word_freq = collections.Counter()

    # letter frequency table
    freq = collections.Counter(text)
    letter_freq += freq

    # total number of letter
    num_letters = 0
    for letter in important_chars:
        num_letters += letter_freq[letter]

    # letters which appear next to themselves, like 'm' in common
    for j, k in zip(text, text[1:]):
        if j == k and j in important_chars:
            di_letter_freq[j] += 1

    #divide on whitespace
    words = text.split()
    freq = collections.Counter(words)
    word_freq += freq

    #word frequency table
    #TODO: strip the '-' word
    unique_words = word_freq.most_common()        #turn the Counter into a list
    one_letter_word_freq = list()                #create separate lists for one,
    two_letter_word_freq = list()                #two and three letter words
    tri_letter_word_freq = list()                #and longer ones, but only if
    long_word_freq = list()                        #they appear multiple times
    #<list>[x][0] gives the key, <list>[x][1] gives the number
    num_words = len(unique_words) #may containg junk such as -

    for i in unique_words:
    #print(i[0], i[1])    #for debugging
        if len(i[0]) == 1:
            one_letter_word_freq.append(i)
        elif len(i[0]) == 2:
            two_letter_word_freq.append(i)
        elif len(i[0]) == 3:
            tri_letter_word_freq.append(i)
        elif i[1] > 1:
            long_word_freq.append(i)
    return list([letter_freq, di_letter_freq, one_letter_word_freq,
                 two_letter_word_freq, tri_letter_word_freq, long_word_freq,
                 num_words, num_letters])
#end get_frequencies()

# TODO: convert to lowercase if args.case == False
def json2python(j):
    """Convert statistics to the needed datastructures"""
    letter_frequencies = collections.defaultdict(lambda: 0)
    letter_frequencies.update(j["letter_frequencies"]["data"])
    di_letter_list = frozenset(j["di_letter_list"]["data"])
    word_list = list()
    word_list.append("")
    word_list.append(frozenset(j["word_list"]["data"]["1"]))
    word_list.append(frozenset(j["word_list"]["data"]["2"]))
    word_list.append(frozenset(j["word_list"]["data"]["3"]))
    word_list.append(frozenset(j["word_list"]["data"]["4"]))
    alphabet = j["alphabet"]
    return list([letter_frequencies, di_letter_list, word_list[1], word_list[2],
                 word_list[3], word_list[4], alphabet])
#end json2python(j)

def how_lang(text, lang):
    """Score how likely is text to be written in lang

          x < -10   very likely
    -10 > x >   0   likely
      0 < x <  10   unlikely
          x >  10   highly improbable"""
    stat = get_frequencies(text, lang[6])

    #TODO: scale expected divergence with length of text
    expected_error = 3
    score = 0

    # punish large differences in letter frequency
    for char in lang[6]:
        # add 0 if the error is smaller than expected error
        score += max(0, abs((stat[0][char]/stat[7])*100 - lang[0][char]) - expected_error)
        #print(letter + " " + str(score)) #for debugging
    # punish diletters not present in English
    # TODO: special case with too many different diletters?
    for i in stat[1]:
        # TODO: Possible problem with SPACELESSTEXT
        #add 3 for each diletter not present in English.
        score += 3 * (not bool(str(i[0]+i[0]) in lang[1]))
        #print(i[0] + i[0] + " " + str(score)) #for debugging
    # reward presence of well known words
    for i in stat[2]:    # TODO: allow lowercase i in case insensitive mode(-c)
        score -= bool(i[0] in lang[2])
    for i in stat[3]:
        score -= bool(i[0] in lang[3])
    for i in stat[4]:
        score -= bool(i[0] in lang[4])
    for i in stat[5]:
        score -= bool(i[0] in lang[5])
    return score
#end how_lang()

def cesar_shift(encrypted, rot, surface):
    """Rotate all alphabetic characters by an equal offset"""
    result = ""
    for i in encrypted:
        if i in surface:
            for j, k in enumerate(surface):
                if i == k:
                    result += surface[(j + rot) % len(surface)]
        else:
    #don't change characters outside the surface
            result += i
    #remove trailing newlines
    #print(type(result)," ", len(result))   #if debug
    while ord(result[-1]) == 10: #'/n' newline
        result = result[:-1]
    return result
#end cesar_shift()

def best_cesar_shift(ciphertext, lang):
    """Try all possible cesar shifts and return the best offset"""
    lowest_score = 100
    shift = 0
    for i in enumerate(lang[6]):
        text = cesar_shift(ciphertext, i[0], lang[6])
        score = how_lang(text, lang)
        lowest_score = min(lowest_score, score)
        if lowest_score == score:
            shift = i[0]
    return shift
# end best_cesar_shift()

def print_stats(text, lang):
    """Output statistics about the text for manual analysis"""
    stat = get_frequencies(text, lang[6])

    #format the frequency table roughly with tabs
#TODO:redo with https://docs.python.org/3.5/library/string.html#format-specification-mini-language
    head = "{a:s}\t{b:s}\t{c:s}\t{d:s}"
    head2 = "{a:s}\t{b:s}\t{c:s}\t{d:s}\t\t{e:s}\t{f:s}\t{g:s}"
    fmt = "{a:s}\t{b:d}\t{c:0.2f}%\t{d:0.2f}%"
    fmt2 = "{a:s}\t{b:d}\t{c:0.2f}%\t{d:0.2f}%\t\t{e:s}\t{f:d}\t{g:b}"

    print(head2.format(a='Letter', b='Times', c='Freq', d='Freq', e='Letter', f='Is', g='Is'))
    print(head2.format(a='', b='in', c='in', d='in', e="Sequ-", f='in', g='in'))
    print(head2.format(a='', b='text', c='text', d='English', e='ence', f='Text', g='English'))

    for char in lang[6]:
        print(fmt2.format(a=char, b=stat[0][char], c=(stat[0][char]/stat[7])*100,
                          d=lang[0][char], e=char+char, f=bool(stat[1][char]),
                          g=bool(char+char in lang[1]))) #if english letters

    print()
    print(head.format(a='Word', b='Times', c='Freq', d='Freq'))
    print(head.format(a='', b='in', c='in', d='in'))
    print(head.format(a='', b='text', c='text', d='English'))
    for i in stat[2]:
        print(fmt.format(a=i[0], b=i[1], c=((i[1]/stat[6])*100), d=0))
    for i in stat[3]:
        print(fmt.format(a=i[0], b=i[1], c=((i[1]/stat[6])*100), d=0))
    for i in stat[4]:
        print(fmt.format(a=i[0], b=i[1], c=((i[1]/stat[6])*100), d=0))
    for i in stat[5]:
        print(fmt.format(a=i[0], b=i[1], c=((i[1]/stat[6])*100), d=0))
    print("Score: " + str(how_lang(text, lang)))

def main(argv=None):
    """Automatically crack simple encryption like the cesar shit cipher"""
    if argv is None:
        argv = sys.argv

    #parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Perform frequency analysis on the passed file')
    parser.add_argument('infile', help="Pass the file you want to analyse",
                        type=argparse.FileType('r', encoding='UTF-8'))
    case = parser.add_mutually_exclusive_group()
    case.add_argument('-c', '--case-insensitive', action="store_true",
                      help="Pass if you want to ignore case(default)",
                      dest="case", default=True)
    case.add_argument('-C', '--case-sensitive', action='store_false',
                      help="Pass if you care about the case",
                      dest="case", default=True)
    parser.add_argument('-l', '--lang', default="lang/english.json",
                        help="Pass the path to a language statistics file",
                        type=argparse.FileType('r', encoding='UTF-8'))
    parser.add_argument('-v', '--verbose', action="count",
                        help="Pass once to print the ciphertext. To be extended")
    args = parser.parse_args()

    # load english frequencies from json
    lang = json2python(json.load(args.lang))

    #letter_frequencies = lang[0]
    #di_letter_list = lang[1]
    #word_list1 = lang[2]
    #word_list2 = lang[3]
    #word_list3 = lang[4]
    #word_list4 = lang[5]
    #alphabet = lang[6]

    # if we use uppercase and lowercase, reflect it in the alphabet
    if not args.case:
        lang[6] = lang[6] + lang[6].upper()

    # get the ciphertext out of the file
    ciphertext = parse_ciphertext(args.infile, args.case, args.verbose)

    # analyse original text
    #stat = get_frequencies(ciphertext, important_chars)

    # decode the ciphertext
    plaintext = cesar_shift(ciphertext, best_cesar_shift(ciphertext, lang), lang[6])

    print_stats(plaintext, lang)

    print("\n" + plaintext)
#end main(argv)

#based on https://www.artima.com/weblogs/viewpost.jsp?thread=4829
if __name__ == "__main__":
    sys.exit(main())
