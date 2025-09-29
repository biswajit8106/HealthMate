from flask import Blueprint, request, jsonify
import numpy as np
import pandas as pd
import pickle
import os

symptom_checker_bp = Blueprint('symptom_checker', __name__)

# Load model data
model_path = os.path.join(os.path.dirname(__file__), "..", "Ai_model", "model.pkl")
with open(model_path, "rb") as f:
    model_data = pickle.load(f)

model = model_data['model']
feature_columns = model_data['columns']
label_encoder = model_data['label_encoder']

# Load additional data
base_path = os.path.join(os.path.dirname(__file__), "..", "Training", "MasterData")
description = pd.read_csv(os.path.join(base_path, "description.csv"))
precautions = pd.read_csv(os.path.join(base_path, "precautions_df.csv"))
medications = pd.read_csv(os.path.join(base_path, "medications.csv"))
workout = pd.read_csv(os.path.join(base_path, "workout_df.csv"))
diets = pd.read_csv(os.path.join(base_path, "diets.csv"))

# Clean columns
description.columns = description.columns.str.strip()
precautions.columns = precautions.columns.str.strip()
diets.columns = diets.columns.str.strip()

# Helper function
def helper(dis):
    desc = description[description['Disease'].str.strip().str.lower() == dis.lower()]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions[precautions['Disease'].str.strip().str.lower() == dis.lower()][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values.flatten()]

    med = medications[medications['Disease'].str.strip().str.lower() == dis.lower()]['Medication']
    med = [m for m in med.values]

    die = diets[diets['Disease'].str.strip().str.lower() == dis.lower()]['Diet']
    die = [d for d in die.values]

    wrkout = workout[workout['disease'].str.strip().str.lower() == dis.lower()]['workout']
    wrkout = [w for w in wrkout.values]

    return desc, pre, med, die, wrkout

# Prediction route
@symptom_checker_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    symptoms = data.get("symptoms", [])

    if len(symptoms) < 2:
        response = {
            "success": False,
            "message": "Please provide at least 2 symptoms."
        }
        return jsonify(response)

    # Create a zero-filled dataframe with the same columns
    test_df = pd.DataFrame(0, index=[0], columns=feature_columns)

    # Set the symptom columns to 1
    for symptom in symptoms:
        if symptom in feature_columns:
            test_df[symptom] = 1
        else:
            print(f"Warning: Symptom '{symptom}' not found in training data and will be ignored.")

    # Ensure the columns are in the same order as during training
    test_df = test_df[feature_columns]

    # Make prediction
    pred_label = model.predict(test_df)[0]
    probs = model.predict_proba(test_df)[0]
    max_prob = np.max(probs)

    if max_prob < 0.1:  # Threshold for low confidence
        response = {
            "success": False,
            "message": "Insufficient confidence in prediction. Please provide more symptoms.",
            "confidence": f"{round(max_prob * 100, 2)}%"
        }
        return jsonify(response)

    # Decode the label back to the original class name
    predicted_disease = label_encoder.inverse_transform([pred_label])[0]
    desc, pre, med, die, wrkout = helper(predicted_disease)

    response = {
        "success": True,
        "predicted_disease": predicted_disease,
        "confidence": round(max_prob, 2),
        "description": desc,
        "precautions": pre,
        "medications": med,
        "diets": die,
        "workouts": wrkout
    }
    return jsonify(response)
