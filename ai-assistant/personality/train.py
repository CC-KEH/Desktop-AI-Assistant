import json
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import ParameterGrid
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from model import NeuralNet
from nltk_utils import tokenize, stem, bag_of_words

# Load intents
with open('makima_intents.json', 'r') as f:
    intents = json.load(f)

# Extract data from intents
all_words = []
tags = []
xy = []

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

# Remove duplicates and ignore characters
ignore = ['?', '.', ',', '!', "'"]
all_words = [stem(w) for w in all_words if w not in ignore]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

# Create input-output pairs
X = []
y = []

for (pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    X.append(bag)
    label = tags.index(tag)
    y.append(label)

X = np.array(X)
y = np.array(y)

class ChatDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# Define hyperparameter grid for tuning
param_grid = {
    'batch_size': [16, 32, 64],
    'hidden_size': [8, 16, 32],
    'learning_rate': [0.001, 0.01, 0.1],
    'num_epochs': [500, 1000]
}

best_model = None
best_score = 0.0
best_params = None
input_size = len(X[0])
output_size = len(tags) + 2  


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# Iterate over all hyperparameter combinations
for params in ParameterGrid(param_grid):
    print(f"Training with hyperparameters: {params}")
    print("\n")
    
    # Create DataLoader
    dataset = ChatDataset(X, y)
    train_loader = DataLoader(dataset=dataset, batch_size=params['batch_size'], shuffle=True)
    
    # Initialize model
    model = NeuralNet(input_size, 
                      params['hidden_size'], 
                      output_size).to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=params['learning_rate'])
    
    # Training loop
    for epoch in range(params['num_epochs']):
        for (words, labels) in train_loader:
            words = words.to(device)
            labels = labels.to(device).long()
            optimizer.zero_grad()
            outputs = model(words)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
    
    # Model evaluation
    predictions = []
    targets = []
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.numpy()
        outputs = model(words)
        _, predicted = torch.max(outputs.data, 1)
        predictions.extend(predicted.cpu().numpy())
        targets.extend(labels)
    
    accuracy = accuracy_score(targets, predictions)
    precision = precision_score(targets, predictions, average='weighted')
    recall = recall_score(targets, predictions, average='weighted')
    f1 = f1_score(targets, predictions, average='weighted')
    
    print(f"Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1-score: {f1}")
    
    # Update best model if necessary
    if f1 > best_score:
        best_score = f1
        best_model = model
        best_params = params

# Save the best model and relevant data
data = {
    "model_state": best_model.state_dict(),
    "input_size": len(X[0]),
    "hidden_size": best_params['hidden_size'],
    "output_size": len(tags),
    "all_words": all_words,
    "tags": tags
}

FILE = "best_model.pth"
torch.save(data, FILE)
print(f"Training Complete. Best model saved to {FILE}. Best hyperparameters: {best_params}")