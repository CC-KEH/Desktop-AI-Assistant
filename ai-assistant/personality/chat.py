import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
import spacy

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
nlp = spacy.load("en_core_web_sm")

function_intents = ["search", "news", "send_message", "run_program", 
                    "play_music", "summarize", "notion","open_site",
                    "ask_question","work","nap","games","search_file",
                    "set_reminder","access_google_services","bored", "control_player"]

# Load intents, jobs, and courses
with open('intents.json', 'r') as f:
    intents = json.load(f)

# Load the pre-trained model and other data
FILE = "makima_v_2.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

# Initialize the model with the same architecture as when it was trained
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Makima"

print(f"{bot_name} here.\n")




def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.80:
        if tag in function_intents:
            return [False, tag]
        
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return [True, random.choice(intent['responses'])]
            
    return [False, "ask_gemini"]

if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(f"{bot_name}: {resp}")