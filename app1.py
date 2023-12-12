import random
import json
import torch
from flask import Flask, render_template, request
from googletrans import Translator

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

translator = Translator(service_urls=['translate.google.com'])

with open('FAQ Chatbot.json', encoding='utf-8') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "BOT"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    message = request.form['message']
    
    if message == "quit":
        return "Chat ended."

    # Detect the language of the message
    detected_language = translator.detect(message).lang

    if detected_language == 'ta':
        # Translate the Tamil message to English
        translated_message = translator.translate(message, dest='en').text

        sentence = tokenize(translated_message)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    response = random.choice(intent['responses'])
                    # Translate the English response to Tamil
                    translated_response = translator.translate(response, src='en', dest='ta').text
                    return translated_response
        else:
            return "மன்னிக்கவும், நீங்கள் தேடும் தகவல்கள் தற்போது என்னிடம் இல்லை. நான் வேறு ஏதாவது உங்களுக்கு உதவ முடியுமா?"

    else:
        sentence = tokenize(message)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    response = random.choice(intent['responses'])
                    return response
        else:
            return "I'm sorry, I don't have the information you're looking for at the moment. Can I assist you with something else?"

if __name__ == '__main__':
    app.run()
