import matplotlib.pyplot as plt

# Données pour HR et HRmulti
tailles = ["2077", "2237", "2397", "2557"]
temps_hr = [171345.0, 9852.0, 974.0, 113.0]
temps_hrmulti = [171658.0, 10125.0, 849.0, 148.0]

# Création du graphique
plt.figure(figsize=(8, 6))
plt.plot(tailles, temps_hr, label='HR', marker='o')
plt.plot(tailles, temps_hrmulti, label='HRmulti', marker='o')

# Titres et légendes
plt.title('Temps d\'exécution HR vs HRmulti pour le dataset "chess"')
plt.xlabel('Taille des données')
plt.ylabel('Temps d\'exécution (ms)')
plt.legend()

# Afficher le graphique
plt.grid(True)
plt.show()
