import csv

fichier = "Device_Dataset.csv"
with open(fichier, 'r') as fichier:
    lecteur_csv = csv.reader(fichier)
    
    # Parcourez les lignes du fichier CSV et affichez-les
    for ligne in lecteur_csv:
        print(ligne)