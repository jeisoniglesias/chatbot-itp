import random
import json
import os
import torch
from src.chat.model.NLPTokenizer import NLPTokenizer
from src.chat.model.model import NeuralNet
from src.chat.train import ChatBotModel


class ChatBot:
    def __init__(
        self,
        intents_path="./src/chat/intents.json",
        model_save_path="data.pth",
        bot_name="Sam",
    ):
        self.intents_path = intents_path
        self.model_save_path = model_save_path
        self.bot_name = bot_name
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = NLPTokenizer()

        self.intents = self.load_intents()
        self.data = self.load_model_data()
        self.model = self.load_model()

    def load_intents(self):
        with open(self.intents_path, "r") as json_data:
            intents = json.load(json_data)
        return intents

    def load_model_data(self):
        if not os.path.exists(self.model_save_path):
            chatbot = ChatBotModel(self.intents_path, self.model_save_path)
            chatbot.run()
        return torch.load(self.model_save_path)

    def load_model(self):
        model = NeuralNet(
            self.data["input_size"], self.data["hidden_size"], self.data["output_size"]
        ).to(self.device)
        model.load_state_dict(self.data["model_state"])
        model.eval()
        return model

    def get_response(self, sentence):
        sentence = self.tokenizer.tokenize(sentence)
        X = self.tokenizer.bag_of_words(sentence, self.data["all_words"])
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self.device)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)

        tag = self.data["tags"][predicted.item()]
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() > 0.75:
            for intent in self.intents["intents"]:
                if tag == intent["tag"]:
                    return random.choice(intent["responses"]), []
        else:
            return False


"""if __name__ == "__main__":
    
"""
