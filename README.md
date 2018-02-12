## Scripts

A bunch of python3 scripts written as I learn the language.
* Caesar decrypts the Caesar cipher, aka. ROT by showing you possible rotations.
* Substitution currently performs letter and word frequency analysis on the file you pass to it. It should eventually get some automated decryption abilities
```
pshem@PC:somewhere/scripts$ ./substitution.py --help
usage: substitution.py [-h] [-c | -C] [-v] infile

This script will perform frequency analysis on the passed file

positional arguments:
  infile                Pass the file you want to analyse

optional arguments:
  -h, --help            show this help message and exit
  -c, --case-insensitive
                        Pass if you want to ignore case(default)
  -C, --case-sensitive  Pass if you care about the case
  -v, --verbose         Pass once to print the ciphertext. To be extended

```
* More scripts may or may not be written later

The scripts were written and used in Python 3.5. They don't work in Python 2.7, and I vaguely remember using something that was added in Python 3.2, so that's probably the minimum version.

®Copyright @pshem and @ZsanettM 2018, Licensed under Apache 2.0
