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
symptom_mapping = {col.lower(): col for col in feature_columns}

# Load additional data
base_path = os.path.join(os.path.dirname(__file__), "..", "Training", "MasterData")
description = pd.read_csv(os.path.join(base_path, "description.csv"))
precautions = pd.read_csv(os.path.join(base_path, "precautions.csv"))
medications = pd.read_csv(os.path.join(base_path, "medications.csv"))
workout = pd.read_csv(os.path.join(base_path, "workouts.csv"))
diets = pd.read_csv(os.path.join(base_path, "diets.csv"))

# Clean columns
description.columns = description.columns.str.strip()
precautions.columns = precautions.columns.str.strip()
medications.columns = medications.columns.str.strip()
workout.columns = workout.columns.str.strip()
diets.columns = diets.columns.str.strip()

# Helper function
def helper(dis):
    desc_filter = description['Disease'].str.strip().str.lower() == dis.lower()
    desc_rows = description[desc_filter]['Description']
    desc = " ".join([str(w) for w in desc_rows]) if not desc_rows.empty else "No description available."

    pre_filter = precautions['Disease'].str.strip().str.lower() == dis.lower()
    pre_rows = precautions[pre_filter]['Precautions']
    if not pre_rows.empty:
        pre_str = str(pre_rows.iloc[0]).strip('"')
        pre = [p.strip() for p in pre_str.split(',')] if pre_str else []
    else:
        pre = ["No precautions available."]
    pre = [p for p in pre if p] or ["No precautions available."]

    med_filter = medications['Disease'].str.strip().str.lower() == dis.lower()
    med_rows = medications[med_filter]['Medications']
    if not med_rows.empty:
        med_str = str(med_rows.iloc[0]).strip('"')
        med = [m.strip() for m in med_str.split(',')] if med_str else []
    else:
        med = ["No medications recommended."]
    med = [m for m in med if m] or ["No medications recommended."]

    die_filter = diets['Disease'].str.strip().str.lower() == dis.lower()
    die_rows = diets[die_filter]['Diets']
    if not die_rows.empty:
        die_str = str(die_rows.iloc[0]).strip('"')
        die = [d.strip() for d in die_str.split(',')] if die_str else []
    else:
        die = ["No diet recommendations."]
    die = [d for d in die if d] or ["No diet recommendations."]

    wrkout_filter = workout['Disease'].str.strip().str.lower() == dis.lower()
    wrkout_rows = workout[wrkout_filter]['Workouts']
    if not wrkout_rows.empty:
        wrkout_str = str(wrkout_rows.iloc[0]).strip('"')
        wrkout = [w.strip() for w in wrkout_str.split(',')] if wrkout_str else []
    else:
        wrkout = ["No workout recommendations."]
    wrkout = [w for w in wrkout if w] or ["No workout recommendations."]

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
        lower_symptom = symptom.lower()
        if lower_symptom in symptom_mapping:
            test_df[symptom_mapping[lower_symptom]] = 1
        else:
            print(f"Warning: Symptom '{symptom}' not found in training data and will be ignored.")

    # Ensure the columns are in the same order as during training
    test_df = test_df[feature_columns]

    # Make prediction
    pred_label = model.predict(test_df)[0]
    probs = model.predict_proba(test_df)[0]
    max_prob = np.max(probs)

    if max_prob < 0.2:  # Threshold for low confidence
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
