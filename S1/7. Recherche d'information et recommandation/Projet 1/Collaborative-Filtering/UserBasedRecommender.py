import os
import time
import gc
import argparse

# data science imports
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.neighbors import NearestNeighbors

# utils import
from fuzzywuzzy import fuzz

class UserBasedRecommender:
    def __init__(self, path_movies, path_ratings):
        self.path_movies = path_movies
        self.path_ratings = path_ratings
        self.movie_rating_thres = 0
        self.user_rating_thres = 0

    def set_filter_params(self, movie_rating_thres, user_rating_thres):
        self.movie_rating_thres = movie_rating_thres
        self.user_rating_thres = user_rating_thres

    def _prep_data(self):
        df_movies = pd.read_csv(
            os.path.join(self.path_movies),
            usecols=['movieId', 'title'],
            dtype={'movieId': 'int32', 'title': 'str'})
        df_ratings = pd.read_csv(
            os.path.join(self.path_ratings),
            usecols=['userId', 'movieId', 'rating'],
            dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})

        df_movies_cnt = pd.DataFrame(
            df_ratings.groupby('movieId').size(),
            columns=['count'])
        popular_movies = list(set(df_movies_cnt.query('count >= @self.movie_rating_thres').index))
        movies_filter = df_ratings.movieId.isin(popular_movies).values

        df_users_cnt = pd.DataFrame(
            df_ratings.groupby('userId').size(),
            columns=['count'])
        active_users = list(set(df_users_cnt.query('count >= @self.user_rating_thres').index))
        users_filter = df_ratings.userId.isin(active_users).values

        df_ratings_filtered = df_ratings[movies_filter & users_filter]

        user_movie_mat = df_ratings_filtered.pivot(
            index='userId', columns='movieId', values='rating').fillna(0)

        del df_movies, df_movies_cnt, df_users_cnt
        gc.collect()

        return user_movie_mat

    def _fuzzy_matching(self, hashmap, fav_movie):
        match_tuple = []
        for title, idx in hashmap.items():
            ratio = fuzz.ratio(title.lower(), fav_movie.lower())
            if ratio >= 60:
                match_tuple.append((title, idx, ratio))

        match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
        if not match_tuple:
            print('Oops! No match is found')
        else:
            print('Found possible matches in our database: {0}\n'.format([x[0] for x in match_tuple]))
            return match_tuple[0][1]

    def _inference(self, user_movie_mat, user_id, n_recommendations):
        user_row = user_movie_mat[user_id]
        user_sim = 1 - pairwise_distances(user_movie_mat, [user_row], metric='correlation')
        user_sim = user_sim.squeeze()

        similar_users = user_sim.argsort()[::-1]
        # Remove the user's own id from the list
        similar_users = [user for user in similar_users if user != user_id]
        recommended_movies = []

        for user in similar_users:
            movies_watched_by_similar_user = user_movie_mat.iloc[user]
            movies_not_watched = movies_watched_by_similar_user[movies_watched_by_similar_user == 0]
            recommended_movies.extend(movies_not_watched.index)

            if len(recommended_movies) >= n_recommendations:
                break

        return recommended_movies[:n_recommendations]

    def make_user_recommendations(self, user_id, n_recommendations):
        user_movie_mat = self._prep_data()
        recommended_movies = self._inference(user_movie_mat, user_id, n_recommendations)

        return recommended_movies

def parse_args():
    parser = argparse.ArgumentParser(
        prog="Movie Recommender",
        description="Run User-Based Movie Recommender")
    parser.add_argument('--path', nargs='?', default='../data/MovieLens',
                        help='input data path')
    parser.add_argument('--movies_filename', nargs='?', default='movies.csv',
                        help='provide movies filename')
    parser.add_argument('--ratings_filename', nargs='?', default='ratings.csv',
                        help='provide ratings filename')
    parser.add_argument('--user_id', type=int, default=1,
                        help='provide user ID for recommendations')
    parser.add_argument('--top_n', type=int, default=10,
                        help='top n movie recommendations')
    return parser.parse_args()

if __name__ == '__main__':
    path_movies = 'movies.csv'  # Remplacez par le chemin complet de votre fichier movies.csv
    path_ratings = 'ratings.csv'  # Remplacez par le chemin complet de votre fichier ratings.csv
    user_id = 1  # L'ID de l'utilisateur pour lequel vous souhaitez des recommandations
    top_n = 10  # Le nombre de recommandations que vous souhaitez obtenir

    recommender = UserBasedRecommender(path_movies, path_ratings)
    recommender.set_filter_params(50, 50)
    recommended_movies = recommender.make_user_recommendations(user_id, top_n)

    print('Top recommendations for User {}:'.format(user_id))
    print(recommended_movies)
