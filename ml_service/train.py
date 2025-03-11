# backend/ml_models/train.py
import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression

# Generate sample data
X = np.array([[i] for i in range(1, 11)])  # Features
y = np.array([2 * i + 3 for i in range(1, 11)])  # Target

# Train a simple linear regression model
model = LinearRegression()
model.fit(X, y)

# Save the model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved as model.pkl")
