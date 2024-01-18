import os
from flask import Flask, render_template, request, jsonify, send_file
import joblib
import numpy as np
import pandas as pd
import sys
sys.path.append("../scripts")
from preprocess_data import *

app = Flask(__name__)

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
app.template_folder = template_dir

lr_model = joblib.load('../models/lr.joblib')
gbr_model = joblib.load('../models/gbr.joblib')
xgbr_model = joblib.load('../models/xgbr.joblib')
rf_model = joblib.load('../models/rf.joblib')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    model_name = request.form['model']
    input_type = request.form['inputType']

    # If user chooses manual entry
    if input_type == 'manual':
        features = [float(request.form[f'sens{i}']) for i in range(1, 16)]
        features = np.array(features).reshape(1, -1)
        # Predict using the selected model
        if model_name == 'lr':
            prediction = lr_model.predict(features)
        elif model_name == 'gbr':
            prediction = gbr_model.predict(features)
        elif model_name == 'xgbr':
            prediction = xgbr_model.predict(features)
        elif model_name == 'rf':
            prediction = rf_model.predict(features)
        else:
            return jsonify({'error': 'Invalid model name'})
        # Render the result template with prediction
        return render_template('result.html', prediction=prediction[0], is_file=False)
    # If user chooses to upload a file
    elif input_type == 'file':
        csv_file = request.files['csvFile']
        df = pd.read_csv(csv_file)

        # Check if the DataFrame and CSV file are not empty
        if not df.empty and not df.isna().all().all():
            df = drop_na(df)
            cols = ['sen1', 'sen2', 'sen3', 'sen4', 'sen5', 'sen6', 'sen7', 'sen8', 'sen9', 'sen10', 'sen11', 'sen12', 'sen13', 'sen14', 'sen15']
            features = df[cols].values
            # Predict using the selected model
            if model_name == 'lr':
                prediction = lr_model.predict(features)
            elif model_name == 'gbr':
                prediction = gbr_model.predict(features)
            else:
                return jsonify({'error': 'Invalid model name'})
            
            # Add predictions to the DataFrame
            df['prediction'] = prediction

            csv_string = str(df.to_csv(index=False))

            # Return the CSV file as a downloadable attachment
            return render_template('result.html', prediction = csv_string, is_file=True)
        else:
            return jsonify({'error': 'DataFrame is empty or contains only NaN values'})
    else:
        return jsonify({'error': 'Invalid input type'})

if __name__ == '__main__':
    port = 8080
    app.run(port=port, debug=True)
