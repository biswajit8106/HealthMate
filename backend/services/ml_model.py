import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os
import logging
from datetime import datetime
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLModel:
    _instance = None

    def __new__(cls, model_path=None):
        if cls._instance is None:
            cls._instance = super(MLModel, cls).__new__(cls)
            cls._instance._initialize(model_path)
        return cls._instance

    def _initialize(self, model_path=None):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.unknown_symptom_value = -1  # Special value for unknown symptoms
        self.model_version = None
        self.model_hash = None

        # Load training data to determine feature count
        data_path = os.path.join(os.path.dirname(__file__), '../../Training/Data/dataset1.csv')
        try:
            data = pd.read_csv(data_path)
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
            encoded_data = np.full(self.num_features, self.unknown_symptom_value)
            for i, symptom in enumerate(symptoms[:self.num_features]):
                try:
                    encoded_data[i] = self.label_encoder.transform([symptom])[0]
                except ValueError:
                    logger.warning(f"Unknown symptom detected: {symptom}. Using default value.")

            # Scale the data
            scaled_data = self.scaler.transform(encoded_data.reshape(1, -1))

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
