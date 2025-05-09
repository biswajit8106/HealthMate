# backend/Training/predict_disease.py

import numpy as np
import pickle

# Load saved model components
model = pickle.load(open("backend/Training/Model/model.pkl", "rb"))
le = pickle.load(open("backend/Training/Model/label_encoder.pkl", "rb"))
symptoms_dict = pickle.load(open("backend/Training/Model/symptom_dict.pkl", "rb"))

def get_predicted_value(user_symptoms):
    input_vector = np.zeros(len(symptoms_dict))

    for symptom in user_symptoms:
        if symptom in symptoms_dict:
            input_vector[symptoms_dict[symptom]] = 1
        else:
            print(f" Warning: '{symptom}' is not recognized and was skipped.")

    # Require at least 3 symptoms to predict
    if np.sum(input_vector) < 3:
        return " Please enter at least 3 valid symptoms."

    pred_idx = model.predict([input_vector])[0]
    return le.inverse_transform([pred_idx])[0]
