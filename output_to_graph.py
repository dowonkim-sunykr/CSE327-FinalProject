import matplotlib.pyplot as plt

# Validation accuracies for epochs 1 to 50
val_acc = [
    63.31, 68.14, 69.69, 70.64, 71.56, 71.03, 70.25, 72.42, 71.39, 70.20,
    71.20, 72.76, 72.91, 71.72, 71.69, 71.95, 72.99, 73.11, 72.28, 72.94,
    72.32, 72.13, 72.37, 72.54, 71.03, 71.95, 71.22, 72.43, 72.56, 70.93,
    72.76, 72.71, 72.35, 73.06, 71.33, 72.23, 73.02, 72.48, 72.43, 72.63,
    72.86, 72.59, 72.78, 71.33, 71.70, 72.40, 73.16, 71.37, 73.04, 72.31
]

epochs = list(range(1, 51))

# Plot Validation Accuracy (Visually styled like your example)
plt.plot(epochs, val_acc, marker='o')
plt.xlabel('Epoch')
plt.ylabel('Accuracy (%)')
plt.title('Validation Accuracy')
plt.ylim(0, 100)
plt.yticks(range(0, 101, 10))
plt.grid(True)
plt.show()
