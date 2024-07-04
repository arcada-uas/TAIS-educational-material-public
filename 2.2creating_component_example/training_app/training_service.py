import numpy as np
import pickle
from sklearn.linear_model import LinearRegression

def train_model(x_train, y_train):
    model = LinearRegression()
    #make x_train 2D
    print("x_train_flat in training service: " + str(x_train))
    x_train = np.array(x_train).reshape(-1, 1)

    print("x_train in training service: " + str(x_train))
    model.fit(x_train, y_train)
    
    #predictions = model.predict(X)
    #rmse = np.sqrt(np.mean((y - predictions) ** 2))

    #turn model into binary format:
    
    return model
