import os
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import time

# Configuration
data_dir = "../my_dataset"
train_dir = os.path.join(data_dir, "train")
val_dir = os.path.join(data_dir, "validation")
batch_size = 64
num_epochs = 100
learning_rate = 0.001
num_classes = len(os.listdir(train_dir))  # Assumes each subfolder is a class
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if torch.cuda.is_available():
    print('cuda')
else:
    print('cpu')

# Transforms
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # ResNet expects 224x224
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],  # Standard ImageNet normalization
                         std=[0.229, 0.224, 0.225])
])

print('about to load dataset')

# Load Datasets
train_dataset = datasets.ImageFolder(root=train_dir, transform=transform)
val_dataset = datasets.ImageFolder(root=val_dir, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

print('done loading dataset')

# Model: Pretrained ResNet18 with final layer modified
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, num_classes)
model = model.to(device)

print('model set')

# Loss and Optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

print('before starting')

# Training Loop
start = time.time()
for epoch in range(num_epochs):
    # print('epoch:', epoch)
    epoch_start = time.time()
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    i = 0
    for images, labels in train_loader:
        # print(i)
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        i += 1

    train_acc = 100 * correct / total
    epoch_end = time.time()
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss:.4f}, Accuracy: {train_acc:.2f}%, Epoch time: {int(epoch_end-epoch_start)}, Time: {int(epoch_end-start)}")

    # Validation
    model.eval()
    val_correct = 0
    val_total = 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            val_total += labels.size(0)
            val_correct += (predicted == labels).sum().item()

    val_acc = 100 * val_correct / val_total
    print(f"Validation Accuracy: {val_acc:.2f}%")

# Save Model
torch.save(model.state_dict(), "resnet18_custom.pth")
print("Model saved as resnet18_custom.pth")
