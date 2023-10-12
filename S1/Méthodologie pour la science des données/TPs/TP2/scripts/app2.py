from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Récupérer le fichier image à partir de la requête
    image_file = request.files.get('image')

    # Vérifier si un fichier a été inclus dans la requête
    if not image_file:
        return jsonify({'error': 'Aucun fichier image n\'a été envoyé'}), 400

    # Effectuer la prédiction sur l'image ici

    # Retourner le résultat de la prédiction
    return jsonify({'prediction': 'Classe prédite'})

if __name__ == '__main__':
    app.run()
