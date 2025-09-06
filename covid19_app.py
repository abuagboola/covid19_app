from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import numpy as np
import logging
import os

app = Flask(__name__)

# Set up logging to file and console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Define the expected features
features = [
    'Sex', 'Fever', 'Cough', 'Headache', 'Runny nose',
    'Difficulty breathing or Dyspnea', 'Fatigue or general weakness',
    'Nausea', 'Diarrhea', 'Chest pain', 'Vomiting'
]

# Check if model file exists
model_path = 'covid_rf_selected_model.pkl'
if not os.path.exists(model_path):
    logging.error(f"Model file '{model_path}' not found")
    model = None
else:
    try:
        model = joblib.load(model_path)
        logging.info("Model loaded successfully")
    except Exception as e:
        logging.error(f"Error loading model: {str(e)}")
        model = None

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        logging.error(f"Error rendering index.html: {str(e)}")
        return jsonify({'error': f'Failed to load page: {str(e)}'}), 500

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        logging.error("Prediction failed: Model not loaded")
        return jsonify({'error': 'Model not loaded. Please check server configuration.'}), 500

    try:
        # Get JSON data from request
        data = request.get_json(force=True)
        logging.debug(f"Received input: {data}")
        
        # Validate input
        if not data:
            logging.warning("No input data provided")
            return jsonify({'error': 'No input data provided'}), 400
        
        # Ensure all required features are present
        missing_features = [f for f in features if f not in data]
        if missing_features:
            logging.warning(f"Missing features: {missing_features}")
            return jsonify({'error': f'Missing features: {missing_features}'}), 400
        
        # Create DataFrame from input
        input_data = pd.DataFrame([data], columns=features)
        
        # Ensure input data is numeric
        try:
            input_data = input_data.astype(float)
        except ValueError as e:
            logging.warning(f"Invalid input data format: {str(e)}")
            return jsonify({'error': f'Invalid input data format: {str(e)}'}), 400
        
        # Validate input values (binary features should be 0 or 1)
        for feature in features:
            if not all(input_data[feature].isin([0, 1])):
                logging.warning(f"Invalid value for {feature}: must be 0 or 1")
                return jsonify({'error': f'Invalid value for {feature}: must be 0 or 1'}), 400
        
        # Predict probability
        proba = model.predict_proba(input_data)[:, 1][0]
        logging.info(f"Prediction successful: Probability = {proba:.2f}")
        
        # Return prediction
        return jsonify({
            'prediction': float(proba),
            'status': 'success',
            'message': f'Likelihood of COVID-19 positive: {proba:.2f}'
        })
    
    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)