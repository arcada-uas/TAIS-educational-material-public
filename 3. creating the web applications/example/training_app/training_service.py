import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

def train_model(x_train, y_train):
    model = LinearRegression()
    x_train = np.array(x_train).reshape(-1, 1)
    model.fit(x_train, y_train)
    
    model_binary = pickle.dumps(model)

    return model_binary
