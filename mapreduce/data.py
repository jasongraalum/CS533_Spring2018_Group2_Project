import json
import random

def splitData(data):
    r = random.sample(range(len(data)), len(data) // 2)
    return (data[r], data[[x for x in range(len(data)) if x not in r]])

def extractData(filename):
    with open(filename) as db:
        for line in [d for d in db if d is not None]:
            yield line

def preprocessGenerator(lines):
    prep = [item for sublist in
                    [data.preprocess(d) for d in lines] if
                        sublist is not None 
                    for item in sublist
                ]
    for l in prep:
        yield l

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

