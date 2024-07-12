import numpy as np
from sklearn.linear_model import LinearRegression

def train_model(x_train, y_train):
    model = LinearRegression()
    #make x_train 2D
    x_train = np.array(x_train).reshape(-1, 1)
    model.fit(x_train, y_train)
    
    return model
