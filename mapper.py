#!/usr/bin/env python
import json
import re
def myMapGenerator(words):
    w = [s for s in words.split(" ") if s is not '']
    return ["%s\t%s" % (word, 1) for word in w]

def map(words):
    l = [item for item in myMapGenerator(words) if len(item) > 0]
    for x in l:
        yield x
