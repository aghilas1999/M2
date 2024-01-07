import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Chargez les données.
movies_dataframe = pd.read_csv("movies.csv")
ratings_dataframe = pd.read_csv("ratings.csv")

# Préparer les données des genres pour la similarité cosinus
movies_dataframe['genres'] = movies_dataframe['genres'].str.replace('|', ' ')
count_vectorizer = CountVectorizer()
genre_matrix = count_vectorizer.fit_transform(movies_dataframe['genres'])
cosine_sim = cosine_similarity(genre_matrix, genre_matrix)

# Créer une fonction pour récupérer les indices de film
movie_indices = pd.Series(movies_dataframe.index, index=movies_dataframe['title']).drop_duplicates()

# Fonction pour avoir les films que l'utilisateur a déjà notés
def find_user_watched_movies(userID):
    user_ratings = ratings_dataframe.query(f"userId == {userID}")
    return user_ratings['movieId'].unique()

print(find_user_watched_movies(1))
'''# Fonction pour recommander des films basés sur la similarité cosinus
def recommend_movies_based_on_content(user_id, num_recommendations=10, movie_indices=movie_indices):
    watched_movie_ids = find_user_watched_movies(user_id)
    
    # Calculez la similarité moyenne de tous les films avec ceux regardés par l'utilisateur
    sim_scores = np.zeros(cosine_sim.shape[0])
    for movieId in watched_movie_ids:
        # Obtenez l'index du film pour la matrice de similarité
        if movies_dataframe[movies_dataframe['movieId'] == movieId].title.values.size > 0:
            idx = movie_indices[movies_dataframe[movies_dataframe['movieId'] == movieId].title.values[0]]
            sim_scores += cosine_sim[idx]

    sim_scores = list(enumerate(sim_scores))
    # Trier les films basés sur les scores de similarité calculés
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Obtenez les scores des 10 films les plus similaires qui n'ont pas été regardés par l'utilisateur
    unwatched_sim_scores = [sim for sim in sim_scores if sim[0] not in watched_movie_ids][:num_recommendations]
    movie_indices = [i[0] for i in unwatched_sim_scores]
    
    # Retournez les films
    return movies_dataframe['title'].iloc[movie_indices]
# Faire des recommandations pour un utilisateur donné

# Demander à l'utilisateur de saisir son ID ou de quitter le programme
while True:
    try:
        user_id = input("Entrez l'ID de l'utilisateur pour lequel vous souhaitez des recommandations ou tapez 'quit' pour quitter: ")
        if user_id.lower() == 'quit':
            break
        
        user_id = int(user_id)  # Convertir l'entrée en un entier
        recommended_movies = recommend_movies_based_on_content(user_id, 10)
        
        print("\nRecommandations pour l'utilisateur", user_id)
        print(recommended_movies)
    except ValueError:
        print("Veuillez entrer un ID valide ou 'quit' pour quitter.")
'''