import os
import argparse

# data science imports
import pandas as pd
import numpy as np



class UserBasedRecommender:
    """
    This is an item-based collaborative filtering recommender with
    KNN implmented by sklearn
    """
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

    def _prep_data(self):
        """
        prepare data for recommender
        """
        # read data
        df_ratings = pd.read_csv(
            os.path.join(self.path_ratings),
            usecols=['userId', 'movieId', 'rating'],
            dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})

        # pivot and create movie-user matrix
        movie_user_mat = df_ratings.pivot(
            index='movieId', columns='userId', values='rating').fillna(0)

        return movie_user_mat

    def _user_similarity(self, data, user_id):
        """
        Calcule la similarité entre les utilisateurs en utilisant la similarité de Pearson.
        
        Parameters
        ----------
        data : numpy array, matrice utilisateur-film

        user_id : int, ID de l'utilisateur pour lequel on veux calculer la similarité
        
        Returns
        -------
        numpy array, matrice de similarité entre l'utilisateur et les autres
        """
    
        user_similarity = []  # Initialisez la liste pour stocker les similarités

        for suser in data.columns:
            # Récupérez les films regardés par l'utilisateur et l'utilisateur similaire
            watched_movies_user = data[user_id][data[user_id] != 0]
            watched_movies_suser = data[suser][data[suser] != 0]
            
            # Calculez l'intersection des films regardés par les deux utilisateurs
            common_movies = np.intersect1d(watched_movies_user.index, watched_movies_suser.index)
            
            # Calculez la similarité si le nombre de films en commun est supérieur ou égal 5
            if len(common_movies) >= 5:
                # Calcul des moyennes des ratings pour les films en commun
                mean_user = watched_movies_user[common_movies].mean()
                mean_suser = watched_movies_suser[common_movies].mean()

                # Calcul des termes supérieurs et inférieurs de la formule de Pearson
                numerator = sum((watched_movies_user[common_movies] - mean_user) * (watched_movies_suser[common_movies] - mean_suser))
                denominator = np.sqrt(sum((watched_movies_user[common_movies] - mean_user) ** 2) * sum((watched_movies_suser[common_movies] - mean_suser) ** 2))

                # Calcul de la similarité de Pearson
                if denominator != 0:
                    pearson_similarity = numerator / denominator
                else:
                    pearson_similarity = 0.0
            else:
                pearson_similarity = 0.0  # Si pas de films en commun, la similarité est 0
            
            user_similarity.append(pearson_similarity)

        user_similarity = np.array(user_similarity)
        return user_similarity  

    def make_user_recommendations(self, user_id, n_recommendations):
        """
        Fait des recommandations basées sur les utilisateurs pour un utilisateur donné.
        
        Parameters
        ----------
        user_id : int, ID de l'utilisateur pour lequel faire des recommandations
        
        n_recommendations : int, nombre de recommandations à générer
        
        Returns
        -------
        list, liste de n_recommendations ID de films recommandés
        """
        # get data
        user_movie_mat = self._prep_data()
        
        # calcule la similarité entre utilisateurs
        user_similarity = self._user_similarity(user_movie_mat, user_id)

        # trouve les utilisateurs similaires
        similar_users = np.argsort(user_similarity)[::-1][1:] + 1  # exclut l'utilisateur lui-même et ajouter 1 car les indices dans la matrice commence par 0.

        # trouve les films non regardés par l'utilisateur donné
        unwatched_movies = user_movie_mat[user_id][user_movie_mat[user_id] == 0]
        #for movie in unwatched_movies.index: print(movie)
        
        # fait des recommandations basées sur les utilisateurs similaires
        recommendations = []

        for movie_id in unwatched_movies.index:
            similarity_sum = 0
            weighted_rating_sum = 0
            for similar_user in similar_users:
                if user_movie_mat[similar_user][movie_id] > 0:  # l'utilisateur similaire a regardé ce film
                    similar_user_mean_rating = np.mean(user_movie_mat[similar_user][user_movie_mat[similar_user] != 0])
                    similarity = user_similarity[similar_user - 1] # car l'indicee commence à 0
                    weighted_rating_sum += similarity * (user_movie_mat[similar_user][movie_id] - similar_user_mean_rating)
                    similarity_sum += np.abs(similarity)
            if similarity_sum > 0:
                user_mean_rating = np.mean(user_movie_mat[user_id][user_movie_mat[user_id] != 0])
                predicted_rating = user_mean_rating + (weighted_rating_sum / similarity_sum)
                recommendations.append((movie_id, predicted_rating))
                print("movie : ", movie_id," predicted rating : ",  predicted_rating)
        
        # trie les recommandations par rating prédit
        recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)
        
        # renvoie les IDs des films recommandés
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
        prog="Movie Recommender",
        description="Run KNN Movie Recommender")
    parser.add_argument('--path', nargs='?', default='../data/MovieLens',
                        help='input data path')
    parser.add_argument('--movies_filename', nargs='?', default='movies.csv',
                        help='provide movies filename')
    parser.add_argument('--ratings_filename', nargs='?', default='ratings.csv',
                        help='provide ratings filename')
    parser.add_argument('--user_id', nargs='?', default='',
                        help='provide your favoriate movie name')
    parser.add_argument('--top_n', type=int, default=10,
                        help='top n movie recommendations')
    return parser.parse_args()


if __name__ == '__main__':
    # get args
    args = parse_args()
    data_path = args.path
    movies_filename = args.movies_filename
    ratings_filename = args.ratings_filename
    user_id = int(args.user_id)  # Ajoutez un argument pour l'ID de l'utilisateur
    top_n = args.top_n
    
    # initial recommender system
    recommender = UserBasedRecommender(
        os.path.join(data_path, movies_filename),
        os.path.join(data_path, ratings_filename))

    # make user recommendations
    recommendations = recommender.make_user_recommendations(user_id, top_n)
    
    # print results
    print(f"Top {top_n} movie recommendations for user {user_id}:")
    for i, movie_id in enumerate(recommendations):
        movie_title = recommender.get_movie_title_by_id(movie_id)  # Ajoutez une méthode pour récupérer le titre du film par ID
        print(f"{i+1}: {movie_title} (MovieID: {movie_id})")