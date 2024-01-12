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
        Prepare data for recommender, including movie genres
        """
        # Read ratings data
        df_ratings = pd.read_csv(
            os.path.join(self.path_ratings),
            usecols=['userId', 'movieId', 'rating'],
            dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})

        # Read movies data to get genres
        df_movies = pd.read_csv(
            os.path.join(self.path_movies),
            usecols=['movieId', 'genres'],
            dtype={'movieId': 'int32', 'genres': 'str'})

        # Merge ratings and movies data on 'movieId'
        df_merged = pd.merge(df_ratings, df_movies, on='movieId')

         # Split genres into a list
        df_merged['genres'] = df_merged['genres'].apply(lambda x: x.split('|'))

        # Create binary columns for each genre using one-hot encoding
        genres_one_hot = df_merged.genres.apply(lambda x: pd.Series(1, index=x)).fillna(0)
        genres_one_hot = genres_one_hot.groupby(df_merged.movieId).sum()
        genres_one_hot = genres_one_hot.applymap(lambda x: 1 if x != 0.0 else 0)

        # Concatenate one-hot encoded genres with the merged dataframe
        df_final = pd.merge(df_merged.drop('genres', axis=1), genres_one_hot, left_on='movieId', right_index=True)

        # Pivot and create movie-user matrix with one-hot encoded genres
        # movie_genre_mat = df_final.pivot_table(
        #     index='movieId', columns='userId', values='rating').fillna(0)
        print('test est passé')
        df_final = df_final.reset_index()
        
        return df_final
        

# Exemple d'utilisation
recommender = ContentRecommendation('movies.csv', 'ratings.csv')
test = recommender._prep_data()
#display(test)
test.to_csv('test.csv',index=True)
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

