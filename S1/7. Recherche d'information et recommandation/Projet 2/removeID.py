import os
import json

# Fonction pour supprimer la clé '_id' d'un fichier JSON
def remove_id_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    if '_id' in data:
        del data['_id']
    
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, separators=(',', ':'))

# Fonction pour parcourir récursivement les fichiers JSON dans un dossier
def process_folder(folder_path):
    print(folder_path)
    for root, dirs, files in os.walk(folder_path):
        print(root)
        for file_name in files:
            if file_name.endswith('.json'):
                print(file_name)
                file_path = os.path.join(root, file_name)
                remove_id_from_json(file_path)

# Chemin du dossier principal à traiter
dossier_principal = 'istex-subset-2023-12-01'

# Appeler la fonction pour traiter le dossier principal
process_folder(dossier_principal)