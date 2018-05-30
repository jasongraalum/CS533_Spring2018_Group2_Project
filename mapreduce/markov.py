import random
def nGrams(words, n = 2):
    if(n < 2):
        yield None
    for k in range(1 - n, len(words) - n + 2):
        if(k < 0):
            l = list(['\r{begin}' for x in range(-k)]) + words[0:k+n]
        elif(k + n > len(words)):
            l = words[k:len(words)] + ['\r{end}']
        else:
            l = words[k:k+n]
        yield tuple(l)

class markovNGramModel:
    n = 2
    def __init__(self, n = 2):
        if(n > 1): 
            self.n = n
        self.defaultStart = tuple(['\r{begin}' for x in range(self.n - 1)])
        self.model = {}

    def update(self, datapoint):
        if(len(datapoint) is not self.n):
            print("Invalid length, no update")
            return
        body = tuple(datapoint[:-1])
        foot = datapoint[-1]
        if body in self.model:
            if foot in self.model[body]:
                self.model[body][foot] += 1
            else:
                self.model[body][foot] = 1
        else:
            self.model[body] = {}
            self.model[body][foot] = 1
        return

    def sampleGen(self, seed = None):
        if(seed is not None):
            samp = [seed] + self.sample((seed,))
        else:
            samp = self.sample()
        sam = samp[:-1]
        sa = " ".join(sam)
        return sa

    def sample(self, seed = None, count = 0):
        if(seed is None):
            seed = self.defaultStart
        choice = random.choice([item for sublist in
                    [[k for _ in range(v)] for k,v in self.model[seed].iteritems()]
                for item in sublist])
        if choice == '\r{end}':
            return [choice]
        else:
            return [choice] + self.sample(seed = tuple(list(seed[1:]) + [choice]), count = count+1)
