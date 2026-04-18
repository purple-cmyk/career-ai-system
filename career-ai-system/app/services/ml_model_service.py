import joblib
import numpy as np
from app.ml_training.features import ALL_FEATURES

model = joblib.load("app/ml_training/satisfaction_model.pkl")

def predict_satisfaction(feature_dict):

    feature_vector = [feature_dict[f] for f in ALL_FEATURES]

    prediction = model.predict([feature_vector])[0]

    return float(prediction)