#!/usr/bin/python
import sys
import mapper
import myReducer
import data
import random
import os
import psutil
import glob
import time
import multiprocessing
import markov

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
        for d in mapd:
            r.reduce(d)
    if debug:
        l = list(r.dictionary.iteritems())
        print("\t{} files processed. Dictionary of {} instances of {} words made".format(len(filenames), sum([v for _,v in l]), len(l)))

def branching(filenames, debug = False):
    if debug:
        print("Data Extraction Split Randomly Over 4 processes:\n    a  \n   / \ \n  b   c\n /\nd")
    outref = os.fork()
    split1 = chunkList(filenames)
    c = random.choice([0,1])
    if outref == 0:
        message = "\tb"
        fns = split1[c]
    else:
        message = "\ta"
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
        print(message + "({})".format(os.getpid()) + ": ({}|{})".format(fn,len(list(r.dictionary.iteritems()))))
    if(inref == 0):
        os._exit(0)
    else:
        os.wait()
        if(outref == 0):
            os._exit(0)
        else:
            os.wait()
    return

def cascade4(filenames, debug = False):
    if debug:
        print("Cascade of 4 processes with queues. read->process->map->reduce")
    lines = [item for sublist in [list(data.extractData(fn)) for fn in filenames] for item in sublist]
    finalDict = {}
    masterq = multiprocessing.Queue()
    lpq = multiprocessing.Queue()
    mapq = multiprocessing.Queue()
    redq = multiprocessing.Queue()

    lineProc = os.fork()
    if lineProc == 0:
        for toProcess in iter(lpq.get, None):
            if(data.preprocess(toProcess) is not None):
                for item in data.preprocess(toProcess):
                    if len(item) > 0:
                        mapq.put(item)
        mapq.put(None)
        time.sleep(0.3)
        os._exit(0)
    else:
        mapProc = os.fork()
        if(mapProc == 0):
            for toMap in iter(mapq.get, None):
                for item in mapper.map(toMap):
                    if len(item) > 0:
                        redq.put(item)
            redq.put(None)
            time.sleep(0.2)
            os._exit(0)
        else:
            reducProc = os.fork()
            if(reducProc == 0):
                r = myReducer.reducer()
                for toReduce in iter(redq.get, None):
                    result = r.onlineReduce(toReduce)
                    masterq.put(result)
                masterq.put(None)
                time.sleep(0.1)
                os._exit(0)
            else:
                for l in lines:
                    lpq.put(l)
                lpq.put(None)
                for k,v in iter(masterq.get, None):
                    finalDict[k] = v
            if debug:
                l = list(finalDict.iteritems())
                print("\t{} files processed. Dictionary of {} instances of {} words made".format(len(filenames), len(l), sum([v for _,v in l])))
            os.wait()
    return

def branchingMarkovCycle(filenames, debug = False, maxIterations = -1, maxTime = 0):
    initialT = time.time()
    procs = listChunks(range(psutil.cpu_count()), 4)
    if debug:
        print("Data extraction then markov chain sampling cycles for {} seconds:\n    a  \n   / \ \n  b   c\n /\nd".format(maxTime))
    outref = os.fork()
    split1 = chunkList(filenames)
    c = random.choice([0,1])
    if outref == 0:
        message = "\tb"
        fns = split1[c]
        op = psutil.Process(os.getpid())
        op.cpu_affinity(procs[0])
#        op.nice(-10)
    else:
        message = "\ta"
        fns = split1[1 - c]
        ip = psutil.Process(os.getpid())
        ip.cpu_affinity(procs[1])
#        ip.nice(-10)
    lines = [item for sublist in [list(data.extractData(fn)) for fn in fns] for item in sublist]
    split2 = chunkList(lines)
    cc = random.choice([0,1])
    inref = os.fork()
    if inref == 0:
        oip = psutil.Process(os.getpid())
        oip.cpu_affinity(procs[2])
#        oip.nice(-10)
        dlines = split2[cc]
        message = "\tc"
        if outref == 0:
            iip = psutil.Process(os.getpid())
            iip.cpu_affinity(procs[3])
            message = "\td"
    else:
        dlines = split2[1 - cc]
    ic = maxIterations
    stopCondition = False;
    nDatapoints = len(dlines)
    prep = [l for l in [data.preprocess(d) for d in dlines] if l is not None]
    split = [item for sublist in [list(data.splitify(line)) for line in prep] for item in sublist]
    while(not stopCondition):
        nGrams = [item for sublist in 
                    [list(markov.nGrams(l)) for l in split] if
                        len(sublist) > 0
                    for item in sublist
                ]
        mod = markov.markovNGramModel()
        for d in nGrams:
            mod.update(d)
        dlines = [mod.sampleGen() for _ in range(nDatapoints)]
        split = [line.split(" ") for line in dlines]
        if(maxIterations >= 0):
            ic -= 1
        if(ic == 0 or time.time() - initialT > maxTime):
            stopCondition = True
    if debug:
        print(message + "({})".format(os.getpid()) + ": ({}|{})".format(fn,len(list(mod.model.iteritems()))))
    if(inref == 0):
        os._exit(0)
    else:
        os.wait()
    if(outref == 0):
        os._exit(0)
    return

def cascadeMarkovMapReduce(filenames, debug = False, maxIterations = -1, maxTime = 0):
    procs = listChunks(range(psutil.cpu_count()), 4)
    if debug:
        print("System of 4 processes with queues. map->reduce->markov->sample, running for {} seconds".format(maxTime))
    #Initial Setup: Get the data from the files and split it up
    lines = [item for sublist in [list(data.extractData(fn)) for fn in filenames] for item in sublist]
    prep = [l for l in [data.preprocess(d) for d in lines] if l is not None]
    datalines = [" ".join(item) for sublist in [list(data.splitify(line)) for line in prep] for item in sublist]
    initialSize = len(datalines)
    finalDict = {}
    dataq = multiprocessing.Queue()
    markovq = multiprocessing.Queue()
    selectq = multiprocessing.Queue()
    redq = multiprocessing.Queue()
    sampleq = multiprocessing.Queue()
    for d in datalines:
        dataq.put(d)

    initialT = time.time()
    redProc = os.fork()
    stopCondition = False;
    if redProc == 0:
        rp = psutil.Process(os.getpid())
        rp.cpu_affinity(procs[0])
#        rp.nice(-10)
        red = myReducer.reducer()
        for toProcess in iter(redq.get, None):
            val = [red.onlineReduce(m) for m in toProcess]
            markovq.put(val)
        markovq.put(None)
        time.sleep(0.3)
        os._exit(0)
    else:
        markovProc = os.fork()
        if(markovProc == 0):
            mp = psutil.Process(os.getpid())
            mp.cpu_affinity(procs[1])
#            mp.nice(-10)
            mod = markov.markovNGramModel()
            for toModel in iter(markovq.get, None):
                for ng in markov.nGrams([w for w,_ in toModel]):
                    mod.update(ng)
                scores = {word : score for word,score in toModel}
                samples = [mod.sampleGen(w,) for w,_ in toModel]
                selectq.put((samples,scores))
            selectq.put(None)
            time.sleep(0.2)
            os._exit(0)
        else:
            selectProc = os.fork()
            if(selectProc == 0):
                sp = psutil.Process(os.getpid())
#                sp.nice(-10)
                r = myReducer.reducer()
                for toScore in iter(selectq.get, None):
                    samples = toScore[0]
                    scores = toScore[1]
                    sampleScores = []
                    for s in [w for w in samples]:
                        total = 0
                        for w in samples:
                            if w in scores:
                                total += scores[w]
                        sampleScores.append(total)
                    scoredSamples = sorted(zip(samples,sampleScores), key=lambda t: t[1])
                    coin = random.choice([1,-1])
                    num = random.choice(range(len(samples)))
                    for winner,score in scoredSamples[:coin*num]:
                        sampleq.put(winner)
                sampleq.put(None)
                time.sleep(0.1)
                os._exit(0)
            else:
                dp = psutil.Process(os.getpid())
#                dp.nice(-10)
                count = 0
                t = 0
                while(count < initialSize):
                    count += 1
                    toProcess = dataq.get()
                    maps = [item for item in mapper.map(toProcess)]
                    redq.put(maps)
                    t = time.time() - initialT
                    if(toProcess is None):
                        stopCondition = True
                if(debug):
                    print("{} examples of real data processed in {} seconds".format(count, t))
                    tick = 0
                while(not stopCondition):
                    if(debug):
                        count += 1
                        t = time.time() - initialT
                        if(tick < t // 1):
                            tick = t // 1
                            print("Sample at {} seconds: {}".format(t, toProcess))
                    if(toProcess is None):
                        stopCondition = True
                    if(t > maxTime):
                        stopCondition = True
                    toProcess = sampleq.get()
                    maps = [item for item in mapper.map(toProcess)]
                    redq.put(maps)
                redq.put(None)
                if debug:
                    print("Last Sample: {}".format(toProcess))
                    print("{} examples used, {} samples generated".format(initialSize, count))
                os.wait()
    return

def cascadeMarkovSameProcess(filenames, debug = False, maxIterations = -1, maxTime = 0):
    procs = listChunks(range(psutil.cpu_count()), 4)
    q = 0
    if debug:
        print("4 markov models passing each other generated data in a cycle, then rebuilding on the new data:\n    a  \n   / \ \n  b   c\n /\nd".format(maxTime))
    dataq = [multiprocessing.Queue() for _ in range(4)]
    outref = os.fork()
    split1 = chunkList(filenames)
    c = random.choice([0,1])
    if outref == 0:
        message = "\tb"
        fns = split1[c]
        op = psutil.Process(os.getpid())
        op.cpu_affinity(procs[0])
        q = 0
#        op.nice(-10)
    else:
        message = "\ta"
        fns = split1[1 - c]
        ip = psutil.Process(os.getpid())
        q = 1
        ip.cpu_affinity(procs[1])
#        ip.nice(-10)
    lines = [item for sublist in [list(data.extractData(fn)) for fn in fns] for item in sublist]
    split2 = chunkList(lines)
    cc = random.choice([0,1])
    inref = os.fork()
    if inref == 0:
        oip = psutil.Process(os.getpid())
        oip.cpu_affinity(procs[2])
        q = 2
#        oip.nice(-10)
        dlines = split2[cc]
        message = "\tc"
        if outref == 0:
            q = 3
            iip = psutil.Process(os.getpid())
            iip.cpu_affinity(procs[3])
            message = "\td"
    else:
        dlines = split2[1 - cc]
    ic = maxIterations
    stopCondition = False;
    nDatapoints = len(dlines)
    prep = [l for l in [data.preprocess(d) for d in dlines] if l is not None]
    split = [item for sublist in [list(data.splitify(line)) for line in prep] for item in sublist]
    dataq[(q + 1) % 4].put(split)
    time.sleep(3)
    initialT = time.time()
    if debug:
        print("Data preprocessing ({}) complete, starting timer".format(q))
    for toProcess in iter(dataq[q].get, None):
        nGrams = [item for sublist in 
                    [list(markov.nGrams(l)) for l in toProcess] if
                        len(sublist) > 0
                    for item in sublist
                ]
        mod = markov.markovNGramModel()
        for d in nGrams:
            mod.update(d)
        dlines = [mod.sampleGen() for _ in range(100)]
        split = [line.split(" ") for line in dlines]
        if(stopCondition):
            time.sleep(0.1)
            dataq[(q + 1) % 4].put(None)
        else:
            if(debug):
                print("{}: Sample: {}".format(q,dlines[0]))
            dataq[(q + 1) % 4].put([line.split(" ") for line in dlines])
        if(maxIterations >= 0):
            ic -= 1
        if(ic == 0 or time.time() - initialT > maxTime):
            stopCondition = True
    time.sleep(0.1)
    dataq[(q + 1) % 4].put(None)
    if debug:
        print(message + "({})".format(os.getpid()) + ": ({}|{})".format(fn,len(list(mod.model.iteritems()))))
    if(inref == 0):
        os._exit(0)
    else:
        os.wait()
    if(outref == 0):
        os._exit(0)
    return

def countdown(x):
    for x in reversed(range(x)):
        print(x + 1)
        time.sleep(1)

filenames = glob.glob("data/*")
print(filenames)
debug = False
maxTime = 60
#singleCore(filenames, debug = debug)
#branching(filenames, debug = debug)
#cascade4(filenames, debug = debug)
print "test 1: Branching with no data sharing"
countdown(3)
branchingMarkovCycle(filenames, debug = debug, maxTime = maxTime)
print "done!"
time.sleep(5)
print "test 2: Sharing data, different processes"
countdown(3)
cascadeMarkovMapReduce(filenames, debug = debug, maxTime = maxTime)
print "done!"
time.sleep(5)
print "test 3: Sharing data, same process"
countdown(3)
cascadeMarkovSameProcess(filenames, debug = debug, maxTime = maxTime)
print "done!"
time.sleep(5)
