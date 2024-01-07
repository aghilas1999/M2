import os
import argparse
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class ContentBasedRecommender:
    def __init__(self, path_movies, path_ratings):
        self.path_movies = path_movies
        self.path_ratings = path_ratings

    def _prep_data(self):
        # Chargement des données
        df_movies = pd.read_csv(
            self.path_movies,
            usecols=['movieId', 'title', 'genres'],
            dtype={'movieId': 'int32', 'title': 'str', 'genres': 'str'})
        
        df_ratings = pd.read_csv(
            self.path_ratings,
            usecols=['userId', 'movieId', 'rating'],
            dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})
        
        return movie_user_mat

    from sklearn.metrics.pairwise import cosine_similarity

    def _user_cosine_similarity(self, data, user_id):
        """
        Calcule la similarité entre les utilisateurs en utilisant la similarité cosinus.
        
        Parameters
        ----------
        data : numpy array, matrice utilisateur-film

        user_id : int, ID de l'utilisateur pour lequel on veut calculer la similarité
        
        Returns
        -------
        numpy array, matrice de similarité entre l'utilisateur et les autres
        """

        # Récupérez les évaluations de l'utilisateur cible
        user_ratings = data.loc[:, user_id].values.reshape(1, -1)

        # Calculez la similarité cosinus entre l'utilisateur cible et tous les autres utilisateurs
        cosine_similarities = cosine_similarity(user_ratings, data.T)

        # Aplatir le tableau de similarités pour le rendre unidimensionnel
        cosine_similarities = cosine_similarities.flatten()

        return cosine_similarities


    def make_content_recommendations(self, user_id, n_recommendations):
    # Obtenez les données
        user_movie_mat = self._prep_data()
        
        # Calculez la similarité entre utilisateurs avec la similarité cosinus
        user_similarity = self._user_cosine_similarity(user_movie_mat, user_id)

        # Trouvez les films non regardés par l'utilisateur donné
        unwatched_movies = user_movie_mat[user_id][user_movie_mat[user_id] == 0]
        
        # Faites des recommandations basées sur les utilisateurs similaires
        recommendations = []

        for movie_id in unwatched_movies.index:
            similarity_sum = 0
            weighted_rating_sum = 0
            for similar_user in np.argsort(user_similarity)[::-1]:  # Parcourir les utilisateurs dans l'ordre de similarité
                if user_movie_mat[similar_user][movie_id] > 0:  # Si l'utilisateur similaire a regardé le film
                    similar_user_mean_rating = np.mean(user_movie_mat[similar_user][user_movie_mat[similar_user] != 0])
                    similarity = user_similarity[similar_user]
                    weighted_rating_sum += similarity * (user_movie_mat[similar_user][movie_id] - similar_user_mean_rating)
                    similarity_sum += np.abs(similarity)

            # Calculez la note prédite pour le film basée sur les utilisateurs similaires
            if similarity_sum > 0:
                user_mean_rating = np.mean(user_movie_mat[user_id][user_movie_mat[user_id] != 0])
                predicted_rating = user_mean_rating + (weighted_rating_sum / similarity_sum)
                recommendations.append((movie_id, predicted_rating))

        # Triez les recommandations par note prédite
        recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)
        
        # Renvoyez les IDs des films recommandés
        return [movie_id for movie_id, _ in recommendations[:n_recommendations]]

    def get_movie_title_by_id(self, movie_id):
            """
            Récupère le titre du film par son ID.
            
            Parameters
            ----------
            movie_id : int, ID du film
            
            Returns
            -------
            str, titre du film
            """

            df_movies = pd.read_csv(
                os.path.join(self.path_movies),
                usecols=['movieId', 'title'],
                dtype={'movieId': 'int32', 'title': 'str'})
                # Recherchez le titre du film correspondant à l'ID donné dans les données de films
            movie_title = df_movies[df_movies['movieId'] == movie_id]['title'].values
                # Vérifiez si le film avec l'ID donné existe
            if len(movie_title) > 0:
                return movie_title[0]
            else:
                return "Film non trouvé"

def parse_args():
    parser = argparse.ArgumentParser(
        prog="Content-Based Movie Recommender",
        description="Run Content-Based Movie Recommender")
    parser.add_argument('--path', nargs='?', default='../Projet4',
                        help='input data path')
    parser.add_argument('--movies_filename', nargs='?', default='movies.csv',
                        help='provide movies filename')
    parser.add_argument('--ratings_filename', nargs='?', default='ratings.csv',
                        help='provide ratings filename')
    parser.add_argument('--user_id', type=int, default=2,
                        help='provide the user ID for recommendations')
    parser.add_argument('--top_n', type=int, default=10,
                        help='number of top recommendations')
    return parser.parse_args()

if __name__ == '__main__':
    # Parse arguments
    args = parse_args()
    data_path = args.path
    movies_filename = args.movies_filename
    ratings_filename = args.ratings_filename
    user_id = args.user_id
    top_n = args.top_n

    # Initialize recommender system
    recommender = ContentBasedRecommender(
        os.path.join(data_path, movies_filename),
        os.path.join(data_path, ratings_filename))

    # Make content-based recommendations
    recommendations = recommender.make_content_recommendations(user_id, top_n)
    
    # Print results
    print(f"Top {top_n} content-based movie recommendations for user {user_id}:")
    for i, movie_id in enumerate(recommendations):
        movie_title = recommender.get_movie_title_by_id(movie_id)  # Ajoutez une méthode pour récupérer le titre du film par ID
        print(f"{i+1}: {movie_title} (MovieID: {movie_id})")