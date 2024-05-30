import json
import torch
import numpy as np
from src.chat.model.ChatDataset import ChatDataset
from src.chat.model.NLPTokenizer import NLPTokenizer
from src.chat.model.model import NeuralNet
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader


class ChatBotModel:
    def __init__(
        self,
        intents_path,
        model_save_path,
        num_epochs=1000,
        batch_size=8,
        learning_rate=0.001,
        hidden_size=8,
    ):
        self.intents_path = intents_path
        self.model_save_path = model_save_path
        self.num_epochs = num_epochs
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.hidden_size = hidden_size

        self.tokenizer = NLPTokenizer()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.intents = self.load_intents()
        self.all_words, self.tags, self.xy = self.prepare_data()
        self.input_size = len(self.all_words)
        self.output_size = len(self.tags)
        self.model = NeuralNet(self.input_size, self.hidden_size, self.output_size).to(
            self.device
        )
        self.dataset = ChatDataset(*self.prepare_training_data())
        self.train_loader = DataLoader(
            dataset=self.dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=0,
        )

    def load_intents(self):
        with open(self.intents_path, "r") as f:
            intents = json.load(f)
        return intents

    def prepare_data(self):
        all_words = []
        tags = []
        xy = []
        for intent in self.intents["intents"]:
            tag = intent["tag"]
            tags.append(tag)
            for pattern in intent["patterns"]:
                w = self.tokenizer.tokenize(pattern)
                all_words.extend(w)
                xy.append((w, tag))
        ignore_words = ["?", ".", "!"]
        all_words = [self.tokenizer.stem(w) for w in all_words if w not in ignore_words]
        all_words = sorted(set(all_words))
        tags = sorted(set(tags))
        return all_words, tags, xy

    def prepare_training_data(self):
        X_train = []
        y_train = []
        for pattern_sentence, tag in self.xy:
            bag = self.tokenizer.bag_of_words(pattern_sentence, self.all_words)
            X_train.append(bag)
            label = self.tags.index(tag)
            y_train.append(label)
        return np.array(X_train), np.array(y_train)

    def train(self):
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate)

        for epoch in range(self.num_epochs):
            for words, labels in self.train_loader:
                words = words.to(self.device)
                labels = labels.to(dtype=torch.long).to(self.device)

                outputs = self.model(words)
                loss = criterion(outputs, labels)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            if (epoch + 1) % 100 == 0:
                print(f"Epoch [{epoch+1}/{self.num_epochs}], Loss: {loss.item():.4f}")

        print(f"Final loss: {loss.item():.4f}")

    def save_model(self):
        data = {
            "model_state": self.model.state_dict(),
            "input_size": self.input_size,
            "hidden_size": self.hidden_size,
            "output_size": self.output_size,
            "all_words": self.all_words,
            "tags": self.tags,
        }
        torch.save(data, self.model_save_path)

    def run(self):
        self.train()
        self.save_model()


"""
if __name__ == "__main__":
    intents_path = "/content/intents.json"
    model_save_path = "data.pth"
    chatbot = ChatBotModel(intents_path, model_save_path)
    chatbot.run()"""
