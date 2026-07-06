import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class SimpleTradingStrategy(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleTradingStrategy, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.softmax(x)
        return x

def generate_dummy_data(num_samples, input_size):
    np.random.seed(42)
    features = np.random.rand(num_samples, input_size).astype(np.float32)
    labels = np.random.randint(0, 2, size=(num_samples,)).astype(np.int64)
    return features, labels

def train_strategy(model, data, labels, epochs=100, learning_rate=0.01):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    for epoch in range(epochs):
        model.train()
        inputs = torch.tensor(data)
        targets = torch.tensor(labels)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}")

def evaluate_strategy(model, data, labels):
    model.eval()
    inputs = torch.tensor(data)
    targets = torch.tensor(labels)
    outputs = model(inputs)
    predictions = torch.argmax(outputs, dim=1)
    accuracy = (predictions == targets).float().mean().item()
    print(f"Accuracy: {accuracy * 100:.2f}%")

if __name__ == '__main__':
    input_size = 5  # Number of features
    hidden_size = 10  # Number of hidden units
    output_size = 2  # Number of classes (buy/sell)
    num_samples = 100  # Number of data points

    # Generate dummy data
    features, labels = generate_dummy_data(num_samples, input_size)

    # Initialize the trading strategy model
    model = SimpleTradingStrategy(input_size, hidden_size, output_size)

    # Train the model
    train_strategy(model, features, labels, epochs=50, learning_rate=0.01)

    # Evaluate the model
    evaluate_strategy(model, features, labels)