import os
import json

# Fonction pour parcourir récursivement les fichiers JSON dans un dossier
def process_folder(folder_path):
    with open("request.txt", 'w', encoding='utf-8') as txt_file:
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith('.json'):
                    print(file_name)
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        for line in file:
                            txt_file.write("{ \"index\" : { \"_index\" : \"aghilas\"} }\n")
                            txt_file.write(line + "\n")

# Chemin du dossier principal à traiter
dossier_principal = 'istex-subset-2023-12-01'

# Appeler la fonction pour traiter le dossier principal
process_folder(dossier_principal)