from fastapi import APIRouter, Depends, HTTPException
import numpy as np
import pandas as pd
import joblib
import os
from models.user_model import User
from database.db import get_db
from utils.auth import get_current_user
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi import Request

router = APIRouter()

class PredictRequest(BaseModel):
    symptoms: list[str]

# Load model data
model_path = os.path.join(os.path.dirname(__file__), "..", "Ai_model", "model.pkl")
model_data = joblib.load(model_path)

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

# Cache disease data for faster lookup
disease_cache = {}
for _, row in description.iterrows():
    disease = row['Disease'].strip().lower()
    disease_cache[disease] = {
        'description': row['Description'].strip(),
        'precautions': precautions[precautions['Disease'].str.strip().str.lower() == disease]['Precautions'].iloc[0] if not precautions[precautions['Disease'].str.strip().str.lower() == disease].empty else '',
        'medications': medications[medications['Disease'].str.strip().str.lower() == disease]['Medications'].iloc[0] if not medications[medications['Disease'].str.strip().str.lower() == disease].empty else '',
        'workouts': workout[workout['Disease'].str.strip().str.lower() == disease]['Workouts'].iloc[0] if not workout[workout['Disease'].str.strip().str.lower() == disease].empty else '',
        'diets': diets[diets['Disease'].str.strip().str.lower() == disease]['Diets'].iloc[0] if not diets[diets['Disease'].str.strip().str.lower() == disease].empty else ''
    }

# Helper function
def helper(dis):
    dis_lower = dis.lower()
    if dis_lower in disease_cache:
        data = disease_cache[dis_lower]
        desc = data['description'] or "No description available."
        pre_str = data['precautions'].strip('"')
        pre = [p.strip() for p in pre_str.split(',')] if pre_str else []
        pre = [p for p in pre if p] or ["No precautions available."]
        med_str = data['medications'].strip('"')
        med = [m.strip() for m in med_str.split(',')] if med_str else []
        med = [m for m in med if m] or ["No medications recommended."]
        die_str = data['diets'].strip('"')
        die = [d.strip() for d in die_str.split(',')] if die_str else []
        die = [d for d in die if d] or ["No diet recommendations."]
        wrkout_str = data['workouts'].strip('"')
        wrkout = [w.strip() for w in wrkout_str.split(',')] if wrkout_str else []
        wrkout = [w for w in wrkout if w] or ["No workout recommendations."]
        return desc, pre, med, die, wrkout
    else:
        return "No description available.", ["No precautions available."], ["No medications recommended."], ["No diet recommendations."], ["No workout recommendations."]

# Prediction route
@router.post("/predict")
async def predict(
    request_data: PredictRequest,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    symptoms = request_data.symptoms

    # Retrieve user data
    user = User.get_user_by_id(db, user_id)

    if len(symptoms) < 2:
        raise HTTPException(status_code=400, detail="Please provide at least 2 symptoms.")

    # Create a zero-filled DataFrame with feature columns
    test_df = pd.DataFrame(0, index=[0], columns=feature_columns)

    # Set the symptom columns to 1
    for symptom in symptoms:
        lower_symptom = symptom.lower()
        if lower_symptom in symptom_mapping:
            test_df[symptom_mapping[lower_symptom]] = 1

    # Make prediction
    pred_label = model.predict(test_df)[0]
    probs = model.predict_proba(test_df)[0]
    max_prob = np.max(probs)

    # Decode the label back to the original class name
    predicted_disease = label_encoder.inverse_transform([pred_label])[0]
    desc, pre, med, die, wrkout = helper(predicted_disease)

    return {
        "success": True,
        "predicted_disease": predicted_disease,
        "confidence": round(max_prob, 2),
        "description": desc,
        "precautions": pre,
        "medications": med,
        "diets": die,
        "workouts": wrkout,
        "user_name": user.name,
        "user_gender": user.gender,
        "user_age": user.age
    }
