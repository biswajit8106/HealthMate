# test/symptom_checker_cli.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.Training.predict_disease import get_predicted_value

if __name__ == "__main__":
    symptoms_input = input("Enter your symptoms (comma-separated): ")
    user_symptoms = [s.strip().lower() for s in symptoms_input.split(",")]

    predicted_disease = get_predicted_value(user_symptoms)
    print("\n🔍 Predicted Disease:", predicted_disease)
