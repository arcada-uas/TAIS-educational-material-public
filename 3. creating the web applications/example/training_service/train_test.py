import json
import numpy as np
from training_service import train_model

def test_train_model():
    # Read the JSON file
    with open('cleaned_data.json', 'r') as f:
        data = json.load(f)

    # Extract x_train and y_train values
    x_train = data['x_train']
    y_train = data['y_train']

    # Call the train_model function
    model_binary = train_model(x_train, y_train)

    with open('model.pkl', 'wb') as f:
        f.write(model_binary)
    

    # Print the result
    print("Model trained and serialized successfully.")
    print(f"Serialized model size: {len(model_binary)} bytes")

if __name__ == "__main__":
    test_train_model()