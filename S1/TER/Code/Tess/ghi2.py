import random
from collections import defaultdict

def read_transactions_from_file(file_path):
    """Lit les transactions depuis un fichier et les retourne comme une liste d'ensembles."""
    transactions = []
    with open(file_path, 'r') as file:
        for line in file:
            items = line.strip().split()  # Convertir la ligne en liste d'items
            transactions.append(set(items))
    return transactions

def sample_transactions(transactions, sample_size):
    """Sélectionne un échantillon aléatoire des transactions."""
    return random.sample(transactions, min(sample_size, len(transactions)))

def count_frequencies(transactions):
    """Compte la fréquence de chaque item dans les transactions."""
    frequency = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            frequency[item] += 1
    return frequency

def estimate_probabilities(frequencies, total_transactions, sample_size):
    """Estime la probabilité que chaque item soit fréquent."""
    probabilities = {}
    for item, freq in frequencies.items():
        sample_probability = freq / sample_size
        estimated_probability = sample_probability * (total_transactions / sample_size)
        probabilities[item] = estimated_probability
    return probabilities

def find_probabilistic_frequent_items(transactions, sample_size, min_support):
    """Trouve les items fréquents dans un ensemble de transactions en utilisant une approche probabiliste."""
    sampled_transactions = sample_transactions(transactions, sample_size)
    frequencies = count_frequencies(sampled_transactions)
    probabilities = estimate_probabilities(frequencies, len(transactions), sample_size)
    
    # Filtrer les items avec une probabilité de fréquence supérieure au seuil de support
    frequent_items = {item: prob for item, prob in probabilities.items() if prob >= min_support}
    return frequent_items

# Chemin du fichier de transactions
file_path = 'ac_200k.dat'

# Lecture des transactions depuis le fichier
transactions = read_transactions_from_file(file_path)

sample_size = 1000  # Taille de l'échantillon pour l'approche probabiliste
min_support = 10  # Seuil de support minimum

frequent_items = find_probabilistic_frequent_items(transactions, sample_size, min_support)
print("Items fréquents estimés :", frequent_items)
