from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
import cv2
import os

app = Flask(__name__)


model = tf.keras.models.load_model("../models/Aghilas_modele.h5")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({'error'})

        # Lire l'image chargé
        image = request.files['image'].read()
        image = np.frombuffer(image, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        image = cv2.resize(image, (224, 224))
        image = image / 255.0

        # Make a prediction using the model
        prediction = model.predict(np.array([image]))

        if prediction > 0.5:
            res = "Pneumonia"
        else:
            res = "Normal"

        return jsonify({'pred': res})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
