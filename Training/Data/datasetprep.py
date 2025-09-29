import pandas as pd
import numpy as np

# --- 1. Load Data and Identify Columns ---
# Assuming the input file is 'dataset1.csv'
FILE_PATH = 'Training\Data\dataset1.csv'
try:
    df = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    print(f"Error: File not found at {FILE_PATH}. Please ensure the file is in the correct directory.")
    exit()

# Extract symptom columns
SYMPTOM_COLS = df.drop(columns=['Prognosis']).columns.tolist()
OUTPUT_FILE = 'enhanced_dataset.csv'
N_INFLUENZA_RECORDS = 15
N_DIABETES_RECORDS = 8

print(f"Starting data enhancement for {len(df)} records...")
print("-" * 50)

# --- 2. Define Clinically Accurate Enhancement Rules ---

# A. Rule: Add high-confidence records for the missing infectious pattern (Influenza/Flu)
# This directly fixes the 19.00% low confidence result.
INFLUENZA_SYMPTOMS = [
    'Body_Pain', 'Joint_Pain', 'Fever', 'Feel_Cold', 'Cough', 'Continuous_Sneezing', 'Headache', 'Nausea'
]

# B. Rule: Add high-confidence records for the chronic pattern (Diabetes)
# This helps the model differentiate it from acute diseases.
DIABETES_SYMPTOMS = [
    'Excessive_Hunger', 'Frequent_Urination', 'Weight_Loss', 'Fatigue', 'Blurred_Vision', 'Tingling_in_hands_and_feet'
]

# --- 3. Programmatic Data Injection ---

new_records = []
zero_row = pd.Series(0, index=SYMPTOM_COLS + ['Prognosis'])

# Inject Influenza Records
for _ in range(N_INFLUENZA_RECORDS):
    record = zero_row.copy()
    for symptom in INFLUENZA_SYMPTOMS:
        if symptom in record.index:
            record[symptom] = 1
    record['Prognosis'] = 'Influenza'
    new_records.append(record)

# Inject Diabetes Differentiation Records
for _ in range(N_DIABETES_RECORDS):
    record = zero_row.copy()
    for symptom in DIABETES_SYMPTOMS:
        if symptom in record.index:
            record[symptom] = 1
    record['Prognosis'] = 'Diabetes'
    new_records.append(record)

df_injected = pd.concat([df, pd.DataFrame(new_records, columns=df.columns)], ignore_index=True)
print(f"Injected {len(new_records)} new clinically defined records.")

# --- 4. Programmatic Data Cleaning (Contradiction Removal) ---

# Clear acute symptoms from chronic diseases (Diabetes, Cancer, Sclerosis, etc.)
CHRONIC_DISEASES = ['Diabetes', 'Cancer', 'Sclerosis', 'Dementia']
ACUTE_SYMPTOMS = ['Fever', 'High_Fever', 'Continuous_Sneezing', 'Feel_Cold', 'Cough']

for disease in CHRONIC_DISEASES:
    for symptom in ACUTE_SYMPTOMS:
        if symptom in df_injected.columns:
            # Set acute symptoms to 0 for chronic disease records
            df_injected.loc[df_injected['Prognosis'] == disease, symptom] = 0

print("Cleaned up acute symptoms from chronic disease records.")


# --- 5. Programmatic Rare Disease Enhancement (Synthetic Addition for SMOTE) ---

# Identify rare diseases again, based on the *initial* distribution
initial_disease_counts = df['Prognosis'].value_counts()
RARE_THRESHOLD = 5 
rare_diseases_to_enhance = initial_disease_counts[initial_disease_counts <= RARE_THRESHOLD].index.tolist()

if rare_diseases_to_enhance:
    print(f"Enhancing {len(rare_diseases_to_enhance)} rare diseases for SMOTE stability...")
    
    # Simple strategy: Add 2 extra records for each rare disease based on their average profile
    rare_enhancement_records = []
    
    for disease in rare_diseases_to_enhance:
        disease_df = df_injected[df_injected['Prognosis'] == disease]
        
        # Calculate the average symptom profile (likelihood of a symptom being 1)
        avg_profile = disease_df[SYMPTOM_COLS].mean()
        
        for i in range(2): # Add 2 synthetic records
            new_record = zero_row.copy()
            # Determine which symptoms to set to 1 based on a probability threshold
            for symptom in SYMPTOM_COLS:
                # Use a random coin flip based on the average profile value
                if np.random.rand() < avg_profile[symptom]:
                    new_record[symptom] = 1
            new_record['Prognosis'] = disease
            
            # Ensure at least one symptom is set, if the average profile was zero
            if new_record[SYMPTOM_COLS].sum() == 0 and not disease_df.empty:
                 # If no symptoms were set, set the most common symptom (if one exists)
                most_common_symptom = disease_df[SYMPTOM_COLS].sum().idxmax()
                if most_common_symptom in new_record.index:
                    new_record[most_common_symptom] = 1
                    
            rare_enhancement_records.append(new_record)

    df_injected = pd.concat([df_injected, pd.DataFrame(rare_enhancement_records, columns=df.columns)], ignore_index=True)
    print(f"Added {len(rare_enhancement_records)} synthetic records for stability.")
else:
    print("No diseases below the rare threshold needed enhancement.")

# --- 6. Save Enhanced Data ---
df_injected.to_csv(OUTPUT_FILE, index=False)
print("-" * 50)
print(f"Data enhancement complete. New dataset saved to: {OUTPUT_FILE}")
print(f"Total records in new dataset: {len(df_injected)}")
