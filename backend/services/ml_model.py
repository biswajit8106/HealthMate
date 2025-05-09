import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from fuzzywuzzy import process
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import os
import json
import logging
from datetime import datetime
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLModel:
    def __init__(self, model_path=None):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.unknown_symptom_value = -1  # Special value for unknown symptoms
        self.model_version = None
        self.model_hash = None

        # Load training data to determine feature count
        data_path = os.path.join(os.path.dirname(__file__), '../../Training/Data/Training.csv')
        try:
            data = pd.read_csv(data_path)
            # Validate feature count
            if data.shape[1] - 1 != 132:
                logger.warning(f"Training data has {data.shape[1] - 1} features, expected 132")
            self.num_features = data.shape[1] - 1  # Last column is target

            # Fit encoder on all possible symptom values from training data
            all_symptoms = data.iloc[:, :-1].values.ravel()
            unique_symptoms = np.unique(all_symptoms)
            self.label_encoder.fit(unique_symptoms)
            self.scaler.fit(data.iloc[:, :-1].values)

            # Generate model version info
            self.model_version = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.model_hash = hashlib.md5(data.to_string().encode()).hexdigest()[:8]
            logger.info(f"Model initialized - Version: {self.model_version}, Data Hash: {self.model_hash}")

        except Exception as e:
            logger.error(f"Error loading training data: {str(e)}")
            raise ValueError("Failed to initialize model - training data could not be loaded")

        if model_path:
            try:
                self.model = joblib.load(model_path)
                # Verify model feature count matches training data
                if hasattr(self.model, 'n_features_in_') and self.model.n_features_in_ != self.num_features:
                    raise ValueError(f"Model expects {self.model.n_features_in_} features but training data has {self.num_features}")
            except Exception as e:
                logger.error(f"Error loading model: {str(e)}")
                raise ValueError("Failed to load model")

    def predict(self, input_vector):
        """Make a prediction based on the input vector."""
        try:
            scaled_data = self.scaler.transform(input_vector.reshape(1, -1))
            predicted_index = self.model.predict(scaled_data)[0]
            predicted_disease = self.label_encoder.inverse_transform([predicted_index])[0]
            return predicted_disease
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            raise ValueError("Prediction failed")

    def diagnose(self, symptoms):
        """Diagnose based on input symptoms."""
        try:
            logger.info(f"Received symptoms for diagnosis: {symptoms}")

            # Convert symptoms to numerical values using the encoder
            encoded_data = []
            for symptom in symptoms:
                try:
                    encoded_data.append(self.label_encoder.transform([symptom])[0])
                except ValueError:
                    logger.warning(f"Unknown symptom detected: {symptom}. Please ensure the symptom is part of the training data.")
                    encoded_data.append(self.unknown_symptom_value)  # Special value for unknown symptoms

            # Ensure input has exactly 132 features, padding with zeros if necessary
            if len(encoded_data) > self.num_features:
                encoded_data = encoded_data[:self.num_features]
            elif len(encoded_data) < self.num_features:
                # Pad with zeros if fewer than 132 features
                padded_data = np.zeros(self.num_features)  # Pad with zeros
                padded_data[:len(encoded_data)] = encoded_data
                encoded_data = padded_data

            # Scale the data
            scaled_data = self.scaler.transform(np.array(encoded_data).reshape(1, -1))

            # Make prediction
            predicted_disease_index = self.model.predict(scaled_data)[0]
            predicted_disease = self.label_encoder.inverse_transform([predicted_disease_index])[0]

            return predicted_disease

        except Exception as e:
            logger.error(f"Error during diagnosis: {str(e)}")
            return {
                'error': 'Diagnosis failed',
                'message': f"An error occurred: {str(e)}"
            }
