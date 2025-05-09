import pandas as pd

# Load your CSV
df = pd.read_csv("backend/Training/MasterData/disease_medication_details_with_timings.csv")

# Define dosage map
dosage_guide = {
    "Omeprazole": "20 mg once daily",
    "Prilosec": "20 mg once daily",
    "Mylanta": "10-20 ml after meals",
    "Fexofenadine": "180 mg once daily",
    "Epinephrine": "0.3 mg injection",
    "Prednisone": "5-10 mg daily",
    "Fluconazole": "150 mg once weekly",
    "Sudafed": "60 mg every 4-6 hours",
    "Candid Multi-Benefit Skin Cream": "Apply twice daily",
    "Udiliv": "300 mg twice daily",
    "Cholstran": "4 g once or twice daily",
    "Ursodeoxycholic acid": "300 mg twice daily",
    "Allergy Relief Antihistamines Tablet": "10 mg daily",
    "Antihistamines": "10 mg at bedtime",
}

# Assign dosages
def get_dosage(med):
    med_lower = med.lower()
    for key in dosage_guide:
        key_lower = key.lower()
        if key_lower in med_lower or med_lower in key_lower:
            return dosage_guide[key]
    return "To be decided"

df["Dosage"] = df["Medicine Name"].apply(get_dosage)

# Save to new CSV
df.to_csv("disease_medication_dosage_timing.csv", index=False)
