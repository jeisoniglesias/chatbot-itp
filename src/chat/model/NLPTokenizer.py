import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize

# Descargar recursos de NLTK si es necesario
nltk.download("punkt")
nltk.download("wordnet")


class NLPTokenizer:
    def __init__(self):
        self.stemmer = PorterStemmer()

    def tokenize(self, sentence):
        """
        Split sentence into array of words/tokens.
        A token can be a word, punctuation character, or number.
        """
        return nltk.word_tokenize(sentence)

    def stem(self, word):
        """
        Stemming = find the root form of the word.
        Examples:
        words = ["organize", "organizes", "organizing"]
        words = [self.stem(w) for w in words]
        -> ["organ", "organ", "organ"]
        """
        return self.stemmer.stem(word.lower())

    def bag_of_words(self, tokenized_sentence, words):
        """
        Return bag of words array:
        1 for each known word that exists in the sentence, 0 otherwise.
        Example:
        sentence = ["hello", "how", "are", "you"]
        words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
        bog   = [  0,    1,    0,   1,    0,    0,      0]
        """
        # Stem each word
        sentence_words = [self.stem(word) for word in tokenized_sentence]
        # Initialize bag with 0 for each word
        bag = np.zeros(len(words), dtype=np.float32)

        # Use a set for faster lookup
        known_words_set = set(words)
        for word in sentence_words:
            if word in known_words_set:
                bag[words.index(word)] = 1

        return bag


"""
# Ejemplo de uso

tokenizer = NLPTokenizer()
sentence = "Hello, how are you?"
tokenized_sentence = tokenizer.tokenize(sentence)
words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
bag = tokenizer.bag_of_words(tokenized_sentence, words)
print(bag)
# Salida: [0. 1. 0. 1. 0. 0. 0.]"""
