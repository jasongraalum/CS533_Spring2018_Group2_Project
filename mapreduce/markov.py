import random
def nGrams(words, n = 2):
    if(n < 2) yield tuple(words)
    for k in range(1 - n, len(words) - n + 1):
        if(k < 0):
            yield tuple(['\r{begin}' for x in range(-k)] + words[0:k+n])
        else if(k + n == len(words)):
            yield tuple(words[k:len(words)] + ['\r{end}'])
        else:
            yield tuple(words[k:k+n])

class markovNGramModel:
    n = 2
    def __init__(self, n = 2):
        if(n > 1): 
            self.n = n
        self.defaultStart = tuple(['\r{begin}' for x in range(self.n - 1)])
        self.model = {}

    def update(self, datapoint):
        if(len(datapoint) < self.n):
            return
        if(len(datapoint) > self.n):
            for n in nGrams(datapoint, self.n)
                self.update(n)
            return
        body = datapoint[:-1]
        foot = datapoint[-1]
        if head in self.model:
            if foot in self.model[head]:
                self.model[head][foot] += 1
            else:
                self.model[head][foot] = 1
        else:
            self.model[head] = {}
            self.model[head][foot] = 1
        return

    def sampleGen(self):
        return " ".join(self.sample()[n:-1])

    def sample(self, seed = self.defaultStart):
        choice = random.choice([item for sublist in
                    [[k for _ in range(v)] for k,v in self.model[seed].iteritems()]
                for item in sublist])
        if choice == '\r{end}':
            return [choice]
        else:
            return [choice] + sample(seed[1:] + choice)
