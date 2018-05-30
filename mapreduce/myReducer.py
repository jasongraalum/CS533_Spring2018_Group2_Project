#!/usr/bin/env python

import sys
from itertools import tee, islice, chain 

class reducer:
    def __init__(self):
        self.dictionary = {}

    def reduce(self, line):
        c=1
        word,count = line.split('\t')
        count = int(count)
        if word in self.dictionary:
            self.dictionary[word] += count
        else:
            self.dictionary[word] = count

    def onlineReduce(self, line):
        self.reduce(line)
        word,count = line.split('\t')
        return (word,self.dictionary[word])

    def merge(self, other):
        for k in other.dictionary:
            if self.dictionary[k] == None:
                self.dictionary[k] = other.dictionary[k]
            else:
                self.dictionary[k] += other.dictionary[k]
