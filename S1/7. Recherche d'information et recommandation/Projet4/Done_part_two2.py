import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from IPython.display import display


class ContentRecommendation:
    def __init__(self, path_movies, path_ratings):
        """
        Recommender requires path to data: movies data and ratings data

        Parameters
        ----------
        path_movies: str, movies data file path

        path_ratings: str, ratings data file path
        """
        self.path_movies = path_movies
        self.path_ratings = path_ratings

    # Une fonction de préparation des données que nous allons utiliser dans la recommandation.
    def _prep_data(self):
        """
        Prepare data for content-based recommender.
        """
        # read data
        movies = pd.read_csv(
            os.path.join(self.path_movies),
            usecols=['movieId', 'genres'],
            dtype={'movieId': 'int32', 'genres': 'str'})

        # Create a matrix where each row represents a movie and each column represents a genre
        vectorizer = CountVectorizer(tokenizer=lambda x: x.split('|'), token_pattern=None)
        genre_matrix = vectorizer.fit_transform(movies['genres'])

        # Add user_id column to the genre_matrix
        user_id_column = np.zeros((genre_matrix.shape[0], 1))  # Create a column of zeros
        genre_matrix_with_user = pd.concat([pd.DataFrame(user_id_column, columns=['userId']), pd.DataFrame(genre_matrix.toarray())], axis=1)

        return genre_matrix_with_user
       

  

# Exemple d'utilisation
recommender = ContentRecommendation('movies.csv', 'ratings.csv')
genre_matrix_with_user = recommender._prep_data()

if genre_matrix_with_user is not None:
    # Vous pouvez afficher la matrice si vous le souhaitez
    display(genre_matrix_with_user)

    # Sauvegarder la matrice dans un fichier CSV
    genre_matrix_with_user.to_csv('resulta.csv', index=False)
    print("Résultat enregistré avec succès dans 'resulta.csv'.")
else:
    print("Erreur: La matrice est None, impossible d'enregistrer le résultat.")





  # def _content_based_user_similarity(self, movie_genre_mat, user_id):
            
    #     """
    #     Calcule la similarité entre les utilisateurs en utilisant la similarité cosinus basée sur le contenu (genres des films).

    #     Parameters
    #     ----------
    #     movie_genre_mat : pandas DataFrame, matrice utilisateur-genre (binaire)

    #     user_id : int, ID de l'utilisateur pour lequel on veut calculer la similarité

    #     Returns
    #     -------
    #     numpy array, matrice de similarité entre l'utilisateur et les autres
    #     """
        
    #     user_similarity = []  # Initialisez la liste pour stocker les similarités

    #     for suser in movie_genre_mat.index:
    #         # Récupérez les genres regardés par l'utilisateur et l'utilisateur similaire
    #         genres_user = movie_genre_mat.loc[user_id]
    #         genres_suser = movie_genre_mat.loc[suser]

    #         # Calculez le nombre de genres en commun
    #         common_genres_count = np.sum((genres_user == 1) & (genres_suser == 1))

    #         # Calculez la similarité cosinus si le nombre de genres en commun est supérieur ou égal à 5
    #         if common_genres_count >= 3:
    #             cosine_similarity = np.dot(genres_user, genres_suser) / (np.linalg.norm(genres_user) * np.linalg.norm(genres_suser))
    #         else:
    #             cosine_similarity = 0.0  # Si moins de 5 genres en commun, la similarité est 0

    #         user_similarity.append(cosine_similarity)

    #     user_similarity = np.array(user_similarity)
    #     return user_similarity

