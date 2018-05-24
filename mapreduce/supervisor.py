#!/usr/bin/python
import sys
import mapper
import myReducer
import data
import random
def singleCore(filenames):
    r = myReducer.reducer()
    for f in filenames:
        lines = list(data.extractData(f))
        prep = [item for sublist in 
                    [data.preprocess(d) for d in lines] if
                        sublist is not None 
                    for item in sublist
                ]
        mapd = [item for sublist in 
                    [list(mapper.map(l)) for l in prep] if
                        len(sublist) > 0
                    for item in sublist
                ]
        for d in mapd:
            r.reduce(d)
    for k in r.dictionary:
        print(k, r.dictionary[k])

def parallel(filenames):
    return

def cascade2():
    return
def cascade4():
    return
filenames = sys.argv[1:len(sys.argv)]
singleCore(filenames)
