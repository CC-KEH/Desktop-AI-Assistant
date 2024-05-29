import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
import spacy


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
nlp = spacy.load("en_core_web_sm")

function_intents = ["search", "news", "send_message", "run_program", "play_music", "summarize", "suggestions","notion","open_site","ask_gpt","get_weather"]
entity_not_required = ["bored", "get_weather","control_player"]
# Load intents, jobs, and courses
with open('intents.json', 'r') as f:
    intents = json.load(f)

# Load the pre-trained model and other data
FILE = "makima_v_1.pth"
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

def extract_entities(sentence):
    doc = nlp(sentence)
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    return entities

def handle_intent(tag,msg):
    entities = extract_entities(msg)
    for entity, label in entities:
        return [tag, entity]

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
            return handle_intent(tag,msg)
        
        elif tag in entity_not_required:
            return [tag]
        
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
            
    return ["ask_gpt", msg]

if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(bot_name+": "+resp)