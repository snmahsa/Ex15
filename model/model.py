import pickle
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import joblib
import os



with open('model/model.pkl', 'rb') as f :
    model = pickle.load(f)

def prediction_iris(features):
    single_sample = np.array(features).reshape(1, -1)
    predictions = model.predict(single_sample)
    return predictions[0]