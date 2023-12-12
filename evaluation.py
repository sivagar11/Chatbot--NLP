import random
import json
import torch
from flask import Flask, render_template, request

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from train import intents , all_words ,tags , model
from app import device



def evaluate_model(model, all_words, tags):
    correct = 0
    total = 0

    with torch.no_grad():
        for intent in intents['intents']:
            for pattern in intent['patterns']:
                sentence = tokenize(pattern)
                X = bag_of_words(sentence, all_words)
                X = X.reshape(1, X.shape[0])
                X = torch.from_numpy(X).to(device)

                output = model(X)
                _, predicted = torch.max(output, dim=1)
                tag = tags[predicted.item()]

                if tag == intent['tag']:
                    correct += 1

                total += 1

    accuracy = correct / total
    return accuracy


accuracy = evaluate_model(model, all_words, tags)
print(f"Accuracy: {accuracy:.2%}")