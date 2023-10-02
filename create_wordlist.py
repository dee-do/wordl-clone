#script to create a wordlist from a text file
#to run this type this in the terminal prompt: 
#python create_wordlist.py wyrdl.py wordlist1.txt

import pathlib
import sys

from string import ascii_letters

#take in the path of the text file to create wordlist from
in_path = pathlib.Path(sys.argv[1])
#take in the path of where you want the newly created file to reside
out_path = pathlib.Path(sys.argv[2])

#sorted takes an iterable and a key to sort on.
#the iterable here is the set of lower case letter words containing a-z characters
#key is a tuple containing 
words = sorted(
    {
        word.lower()
        for word in in_path.read_text(encoding="utf-8").split()
        #filter out non ascii characters, i.e. allow a-z
        if all(letter in ascii_letters for letter in word)

    },
    #key will be assigned a tuple containing the length of the word and the word itself
    #this is then used for sorting
    key = lambda word: (len(word), word)
)

#write the words separated by a new line to the path specified in out_path
out_path.write_text("\n".join(words))