import random
import glob
import sys

"""
Markov Babbler

After being trained on text from various authors, can
'babble', or generate random walks, and produce text that
vaguely sounds like the author.
"""

class Babbler:
    def __init__(self, n, seed=None):
        self.n = n
        if seed != None:
            random.seed(seed)
        # TODO: your code goes here
        #create a dictionary
        self.dict = {"Starter" : [], "Stopper" : []};

    
    def add_sentence(self, sentence):
        list = sentence.lower().split();
        n = self.n;
        if(len(list) == 0): #check empty file input
            raise FileNotFoundError;

        if(len(list) < n): #check if bigram can be form
            raise ValueError;

        pointer = "Starter"
        for x in range(len(list)- n + 1 ):
            grams = " ".join(list[x:x+n]);
            if x == len(list) - n: #check if at the end
                self.dict["Stopper"].append(grams);
                if not grams in self.dict.keys():
                    self.dict[grams] = [];

                self.dict[grams].append('EOL')

            self.dict[pointer].append(grams);
            if not grams in self.dict and not grams in self.dict["Stopper"]:
                self.dict[grams] = [];
            pointer = grams;
        pass

    
    def add_file(self, filename):
        for line in [line.rstrip().lower() for line in open(filename, errors='ignore').readlines()]:
            self.add_sentence(line)


    def get_starters(self):
        return self.dict["Starter"];
    

    def get_stoppers(self):
        return self.dict["Stopper"];


    def get_successors(self, ngram):
        if not self.has_successor(ngram):
            raise ValueError;

        possible = [];
        for x in self.dict[ngram]:
            placebo = list(x.split());
            possible.append(placebo[len(placebo) - 1]);

        return possible;
        pass
    

    def get_all_ngrams(self):
        print(self.dict);
        dictList = list(self.dict.keys());
        return(dictList[2: len(dictList)]);
        pass

    
    def has_successor(self, ngram):
        if not ngram in self.dict.keys():
            return False;
        if not self.dict[ngram]:
            return False;
        return True;
        pass
    
    
    def get_random_successor(self, ngram):
        if self.has_successor(ngram):
            return random.choice(self.dict[ngram]);
        raise ValueError;
    

    def babble(self):
        starting = random.choice(self.dict["Starter"]);
        babble = starting.split()[0];
        starting = random.choice(self.dict[starting]);
        while not starting in self.dict["Stopper"] :
            babble = babble +  " " + starting.split()[0]; #always 0 0 no matter n grams
            starting = random.choice(self.dict[starting]);



        return babble + " " + starting;
        pass
            

def main(n=2, filename='tests/test1.txt', num_sentences=5):
    """
    Simple test driver.
    """
    print(filename)
    babbler = Babbler(n)
    babbler.add_file(filename)
    print(f'num starters {len(babbler.get_starters())}')
    print(f'num ngrams {len(babbler.get_all_ngrams())}')
    print(f'num stoppers {len(babbler.get_stoppers())}')
    for _ in range(num_sentences):
        print(babbler.babble())




if __name__ == '__main__':
    # remove the first parameter, which should be babbler.py, the name of the script
    sys.argv.pop(0)
    n = 2
    filename = 'tests/test2.txt'
    num_sentences = 5
    if len(sys.argv) > 0:
        n = int(sys.argv.pop(0))
    if len(sys.argv) > 0:
        filename = sys.argv.pop(0)
    if len(sys.argv) > 0:
        num_sentences = int(sys.argv.pop(0))
    main(n, filename, num_sentences)
