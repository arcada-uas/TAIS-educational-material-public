import pickle
import json
import numpy as np
from datetime import datetime
from test_service import test_model

def test_test_model():
    # Load the model from the pickle file
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)

    # Load the test data from the JSON file
    with open('cleaned_data.json', 'r') as file:
        test_data = json.load(file)

    # Extract and convert the test data
    x_test = np.array(test_data['x_test'])
    y_test = np.array(test_data['y_test'])
    dates_test = [datetime.strptime(date, '%Y-%m-%d') for date in test_data['dates_test']]

    # Call the test_model function
    test_model(model, x_test, y_test, dates_test)

    # Check the output (this can be more sophisticated with assertions)
    print("Test completed successfully.")

# Run the test function
if __name__ == "__main__":
    test_test_model()