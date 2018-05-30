#!/usr/bin/env python
import json
import re
def splitGen(words):
    for s in [w for w in words.split(" ")]:
        yield s

def map(words):
    for word in splitGen(words):
        yield "%s\t%s" % (word, 1) 

#    l = [item for item in myMapGenerator(words) if len(item) > 0]
#    for x in l:
#        yield x
