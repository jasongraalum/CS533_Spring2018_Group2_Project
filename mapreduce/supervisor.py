#!/usr/bin/python
import sys
import mapper
import myReducer
import data
import random
import os
import psutil
import time
import multiprocessing
def listChunks(l, n = 2):
    c = []
    x = len(l) // n
    while(len(c) < n - 1):
        c.append(list(range(len(l))[(len(c) * x) // 1 : ((len(c) + 1) * x) // 1]))
    c.append(list(range(len(l))[len(c) * x : ]))
    return c

def randomizedListChunks(l, n = 2):
    c = []
    k = len(l) // n
    while(len(c) < n - 1):
        c.append(random.sample([i for i in range(len(l)) if i not in [item for sublist in c for item in sublist]], k))
    c.append([i for i in range(len(l)) if i not in [item for sublist in c for item in sublist]])
    return c

def chunkList(l, random = True, n = 2):
    if(random):
        return [[l[i] for i in c] for c in randomizedListChunks(l, n)]
    else:
        return [[l[i] for i in c] for c in listChunks(l, n)]

def singleCore(filenames, debug = False):
    if debug:
        print("One process")
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
        r = myReducer.reducer()
        for d in mapd:
            r.reduce(d)
    if debug:
        l = list(r.dictionary.iteritems())
        print("\t{} files processed. Dictionary of {} instances of {} words made".format(len(filenames), len(l), sum([v for _,v in l])))

def branching(filenames, debug = False):
    if debug:
        print("Data Extraction Split Randomly Over 4 processes:\n    a  \n   / \ \n  b   c\n /\nd")
    outref = os.fork()
    split1 = chunkList(filenames)
    c = random.choice([0,1])
    if outref == 0:
        message = "\ta"
        fns = split1[c]
    else:
        message = "\tb"
        fns = split1[1 - c]
    lines = [item for sublist in [list(data.extractData(fn)) for fn in fns] for item in sublist]
    split2 = chunkList(lines)
    cc = random.choice([0,1])
    inref = os.fork()
    if inref == 0:
        dlines = split2[cc]
        message = "\tc"
        if outref == 0:
            message = "\td"
    else:
        dlines = split2[1 - cc]
    prep = [item for sublist in 
                [data.preprocess(d) for d in dlines] if
                    sublist is not None 
                for item in sublist
            ]
    mapd = [item for sublist in 
                [list(mapper.map(l)) for l in prep] if
                    len(sublist) > 0
                for item in sublist
            ]
    r = myReducer.reducer()
    for d in mapd:
        r.reduce(d)
    if debug:
        printList = ["({} : {})".format(k,v) for k,v in random.sample(list(r.dictionary.iteritems()), 3)]
        print(message + "({})".format(os.getpid()) + ": ({}|{}) {}".format(fn,len(list(r.dictionary.iteritems())),printList))
    if(inref != 0):
        os.wait()
        if(outref != 0):
            os.wait()

def cascade4(filenames, debug = False):
    if debug:
        print("Cascade of 4 processes with queues. read->process->map->reduce")
    lines = [item for sublist in [list(data.extractData(fn)) for fn in filenames] for item in sublist]
    finalDict = {}
    masterq = multiprocessing.Queue()
    lpq = multiprocessing.Queue()
    lineProc = os.fork()
    if lineProc == 0:
        mapq = multiprocessing.Queue()
        time.sleep(0.2)
        mapProc = os.fork()
        if mapProc == 0:
            redq = multiprocessing.Queue()
            time.sleep(0.2)
            reducer = os.fork()
            if(reducer == 0):
                r = myReducer.reducer()
                for toReduce in iter(redq.get, None):
                    result = r.onlineReduce(toReduce)
                    masterq.put(result)
                masterq.put(None)
            else:
                for toMap in iter(mapq.get, None):
                    for item in mapper.map(toMap):
                        redq.put(item)
                redq.put(None)
        else:
            for toProcess in iter(lpq.get, None):
                if(data.preprocess(toProcess) is not None):
                    for item in data.preprocess(toProcess):
                        mapq.put(item)
            mapq.put(None)
    else:
        for l in lines:
            lpq.put(l)
        lpq.put(None)
        for k,v in iter(masterq.get, None):
            finalDict[k] = v
        if debug:
            for k,v in finalDict.iteritems():
                print(k,v)

filenames = sys.argv[1:len(sys.argv)]
debug = True
singleCore(filenames, debug = debug)
branching(filenames, debug = debug)
cascade4(filenames, debug = debug)
