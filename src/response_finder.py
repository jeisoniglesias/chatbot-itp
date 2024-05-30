import json
import random
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download("punkt")
nltk.download("wordnet")


class ResponseFinder:
    def __init__(self, json_path):
        self.lemmatizer = WordNetLemmatizer()
        self.data = self.load_json(json_path)

    def load_json(self, path):
        with open(path, encoding="utf-8") as file:
            return json.load(file)

    def find_response(self, message):
        message = message.lower()
        message_words = nltk.word_tokenize(message)
        message_lemmas = [self.lemmatizer.lemmatize(word) for word in message_words]

        best_match = {"tag": "desconocido", "score": 0}
        for intent in self.data["intents"]:
            for pattern in intent.get("patterns", []):
                pattern_words = nltk.word_tokenize(pattern)
                pattern_lemmas = set(
                    [self.lemmatizer.lemmatize(word) for word in pattern_words]
                )
                score = sum(1 for lemma in message_lemmas if lemma in pattern_lemmas)
                if score > best_match["score"]:
                    best_match = {"tag": intent["tag"], "score": score}

        if best_match["tag"] == "desconocido" or best_match["score"] == 0:
            # response = random.choice(["Lo siento, no entiendo tu pregunta. ¿Puedes reformularla?"])
            # follow_up = []
            return False, []

        else:
            for intent in self.data["intents"]:
                if intent["tag"] == best_match["tag"]:
                    response = random.choice(intent["responses"])
                    follow_up = intent.get("follow_up", [])
                    break
        print(response, follow_up)
        return response, follow_up
