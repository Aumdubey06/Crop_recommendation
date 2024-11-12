from flask import Flask, request, jsonify, render_template
import joblib
from flask_cors import CORS
import numpy as np
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load the Random Forest model
try:
    random_forest_model = joblib.load('models/random_forest_model.pkl')
    print("Random Forest model loaded successfully.")
except Exception as e:
    print("Model loading error:", e)
    traceback.print_exc()

# Define a mapping from numeric labels to crop names
crop_mapping = {
    0: 'rice',
    1: 'maize',
    2: 'jute',
    3: 'cotton',
    4: 'coconut',
    5: 'papaya',
    6: 'orange',
    7: 'apple',
    8: 'muskmelon',
    9: 'watermelon',
    10: 'grapes',
    11: 'mango',
    12: 'banana',
    13: 'pomegranate',
    14: 'lentil',
    15: 'blackgram',
    16: 'mungbean',
    17: 'mothbeans',
    18: 'pigeonpeas',
    19: 'kidneybeans',
    20: 'chickpea',
    21: 'coffee'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("Received data:", data)  # Print received data for debugging

        # Extract feature values, converting empty fields to a default value of 0
        nitrogen = float(data.get("nitrogen", 0) or 0)
        phosphorus = float(data.get("phosphorus", 0) or 0)
        potassium = float(data.get("potassium", 0) or 0)
        temperature = float(data.get("temperature", 0) or 0)
        humidity = float(data.get("humidity", 0) or 0)
        ph = float(data.get("ph", 0) or 0)
        rainfall = float(data.get("rainfall", 0) or 0)

        # Encode region as a one-hot vector
        region = data.get("region", "")
        regions = ["Central India", "Eastern India", "North Eastern India", "Northern India", "Other", "Western India"]
        region_encoded = [1 if region == r else 0 for r in regions]

        # Combine all features into a single array
        features = np.array([nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall] + region_encoded).reshape(1, -1)
        
        # Make prediction with the Random Forest model
        crop_prediction = random_forest_model.predict(features)[0]

        # Get the crop name from the crop mapping
        crop_name = crop_mapping.get(crop_prediction, "Unknown Crop")

        # Return the crop name in the JSON response
        return jsonify({"crop_recommendation": crop_name})
    except ValueError as e:
        print("Value error:", e)
        return jsonify({"error": "Invalid input values. Please make sure all inputs are numbers."}), 400
    except Exception as e:
        # Log the full traceback for debugging
        print("Prediction error:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
