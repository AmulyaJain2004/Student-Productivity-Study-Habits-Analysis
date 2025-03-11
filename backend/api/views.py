import os
import pickle
import numpy as np
from django.http import JsonResponse
from rest_framework.decorators import api_view

# Define model path
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../ml_service/models/model.pkl")

# Load the model only if it exists
model = None
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
else:
    print(f"Warning: Model file not found at {MODEL_PATH}")

@api_view(["POST"])
def predict(request):
    if model is None:
        return JsonResponse({"error": "Model file not found. Please train the model first."}, status=500)

    try:
        data = request.data  # Expecting JSON { "input": [5] }
        input_features = np.array(data["input"]).reshape(-1, 1)
        prediction = model.predict(input_features)
        return JsonResponse({"prediction": prediction.tolist()})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
