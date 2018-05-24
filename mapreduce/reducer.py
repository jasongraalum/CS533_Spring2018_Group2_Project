#!/usr/bin/env python

import sys

curWord = None
curCount = 0
word = None

for line in sys.stdin:
    line = line.strip()
    word, count = line.split('\t')
    try:
        count = int(count)
    except ValueError:
        continue

    if curWord == word:
        curCount += count
    else:
        if curWord:
            print "%s\t%s" % (curWord, curCount)
        curCount = count
        curWord = word

if curWord == word:
    print "%s\t%s" % (curWord, curCount)
    
