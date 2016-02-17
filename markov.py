#!/usr/bin/python

import random

class TransitionEntry:
    def __init__(self, word):
        self.word = word
        self.count = 1

class MarkovChainGenerator:
    def __init__(self):
        self.lookup = {}
        self.PUNCTUATION = [".", "!", "?"]

        print "Initializing..."
        self.loadReference()
        self.configureCapitalizationAndPunctuation()
        print "...Finished"

    def loadReference(self, reference="references/default.txt"):
        currentState = None
        nextState = None

        with open(reference) as f:
            for line in f:
                tokens = line.split()

                if currentState is None and len(tokens) > 0:
                    currentState = tokens.pop(0)

                # For each word, create a transition from
                # the current state. After, advance
                # the current state to the next state
                while len(tokens) > 0:
                    nextState = tokens.pop(0)

                    currentEntry = self.lookup.get(currentState)

                    if currentEntry is None:
                        self.lookup[currentState] = {}
                        currentEntry = self.lookup[currentState]

                    nextEntry = currentEntry.get(nextState)

                    if nextEntry is None:
                        currentEntry[nextState] = TransitionEntry(nextState)
                    else:
                        nextEntry.count += 1

                    currentState = nextState

    def configureCapitalizationAndPunctuation(self):
        self.capitalizedWords = []
        self.hasPunctuation = False

        # Check for capitalization and punctuation
        for key in self.lookup.keys():
            if key.istitle():
                self.capitalizedWords.append(key)

            if key[-1] in self.PUNCTUATION:
                self.hasPunctuation = True

    def getStartOfSentence(self):
        # If there is no capitalization, just pick a random
        # word to start from
        if len(self.capitalizedWords) > 0:
            return random.choice(self.capitalizedWords)
        else:
            return random.choice(self.lookup.keys())

    def isEndOfSentence(self, word):
        # If there is no punctuation, just let the sentence be a run-on
        if not self.hasPunctuation:
            return False

        return word[-1] in self.PUNCTUATION

    def generate(self, sentenceThreshold=1, wordThreshold=50):
        nSentences = 0
        nWords = 0
        output = ""

        currentWord = self.getStartOfSentence()

        while True:
            output += currentWord + " "
            nWords += 1

            # Do we have enough words to call it a day?
            if nWords >= wordThreshold:
                break

            # Check if this word has punctuation
            if self.isEndOfSentence(currentWord):
                nSentences += 1

                # Have we reached our sentence quota
                if nSentences >= sentenceThreshold:
                    break

                # We have reached the end of the sentence, so let's
                # grab a new random word to start a new sentence
                currentWord = self.getStartOfSentence()
                continue

            try:
                words = self.lookup[currentWord]
            except:
                # There are no words that follow this word,
                # end the output
                break

            possibilities = []

            for k, word in words.iteritems():
                for i in range(0, word.count):
                    possibilities.append(word.word)

            # Choose next word
            currentWord = random.choice(possibilities)

        print output

if __name__ == "__main__":
    markov = MarkovChainGenerator()
    markov.generate()
