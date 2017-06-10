#!/usr/bin/python
import random


class TransitionEntry(object):
    def __init__(self, word):
        self.word = word
        self.count = 1


class MarkovChainGenerator(object):

    PUNCTUATION = [".", "!", "?"]

    def __init__(self, reference="references/default.txt"):
        self.lookup = {}

        print "Initializing..."
        self.load_reference(reference)
        self.configure_capitalization_and_punctuation()
        print "...Finished"

    def load_reference(self, reference):
        current_state = None
        next_state = None

        with open(reference) as input_file:
            for line in input_file:
                tokens = line.split()

                if current_state is None and len(tokens) > 0:
                    current_state = tokens.pop(0).lower()

                # For each word, create a transition from
                # the current state. After, advance
                # the current state to the next state
                while len(tokens) > 0:
                    next_state = tokens.pop(0).lower()

                    current_entry = self.lookup.get(current_state)

                    if current_entry is None:
                        self.lookup[current_state] = {}
                        current_entry = self.lookup[current_state]

                    next_entry = current_entry.get(next_state)

                    if next_entry is None:
                        current_entry[next_state] = TransitionEntry(next_state)
                    else:
                        next_entry.count += 1

                    current_state = next_state

    def configure_capitalization_and_punctuation(self):
        self.capitalized_words = []
        self.has_punctuation = False

        # Check for capitalization and punctuation
        for key in self.lookup:
            if key.istitle():
                self.capitalized_words.append(key)

            if key[-1] in self.PUNCTUATION:
                self.has_punctuation = True

    def get_start_of_sentence(self):
        # If there is no capitalization, just pick a random
        # word to start from
        if len(self.capitalized_words) > 0:
            return random.choice(self.capitalized_words)
        else:
            return random.choice(self.lookup.keys())

    def is_end_of_sentence(self, word):
        # If there is no punctuation, just let the sentence be a run-on
        if not self.has_punctuation:
            return False

        return word[-1] in self.PUNCTUATION

    def generate(self, sentence_threshold=1, word_threshold=50):
        num_sentences = 0
        num_words = 0
        output = ""

        current_word = self.get_start_of_sentence()

        while True:
            output += current_word + " "
            num_words += 1

            # Do we have enough words to call it a day?
            if num_words >= word_threshold:
                break

            # Check if this word has punctuation
            if self.is_end_of_sentence(current_word):
                num_sentences += 1

                # Have we reached our sentence quota
                if num_sentences >= sentence_threshold:
                    break

                # We have reached the end of the sentence, so let's
                # grab a new random word to start a new sentence
                current_word = self.get_start_of_sentence()
                continue

            try:
                words = self.lookup[current_word]
            except KeyError:
                # There are no words that follow this word,
                # end the output
                break

            possibilities = []

            for word in words.itervalues():
                for _ in range(0, word.count):
                    possibilities.append(word.word)

            # Choose next word
            current_word = random.choice(possibilities)

        print output

if __name__ == "__main__":
    markov = MarkovChainGenerator(reference="references/default.txt")
    markov.generate()
