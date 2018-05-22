#!/usr/bin/env python
import json
import re
def myMap(words):
    return ["%s\t%s" % (word, 1) for word in words if re.match(r'^#[a-z0-9]',word)]

def preprocess(line):
    line = line.strip() #strips out the data with parameter passed in the paranthesis
    line = json.loads(line)
    try:
        line = line['text']  # extract the tweet
        words = line.encode('ascii', 'ignore') # handle non-ascii values
        words = words.lower()
    except KeyError:
        return None
    return words.split('\n')

def doMap(filenames):
    for name in filenames:
        yield [item for sublist in [myMap(words) for words in [preprocess(line) for line in extractData(filenames) if line is not None] if words is not None] for item in sublist]
