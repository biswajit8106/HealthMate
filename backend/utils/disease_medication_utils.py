import csv
import os

csv_file_path = os.path.join(os.path.dirname(__file__), '..', 'Training', 'MasterData', 'disease_medication_details_with_timings.csv')

def load_disease_medication_data():
    disease_med_map = {}
    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)
        # Strip fieldnames to remove extra spaces
        reader.fieldnames = [field.strip() for field in reader.fieldnames]
        for row in reader:
            disease = row['Disease'].strip()
            medicine = row['Medicine Name'].strip()
            dosage = row['Dosage'].strip()
            timing = row['Timing'].strip()
            key = (disease.lower(), medicine.lower())
            disease_med_map[key] = {
                'dosage': dosage,
                'timing': timing
            }
    return disease_med_map

# Load once at module import
disease_medication_data = load_disease_medication_data()
