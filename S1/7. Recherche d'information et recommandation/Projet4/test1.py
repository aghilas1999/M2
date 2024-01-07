import pandas as pd
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity

class ContentBasedFiltering:
    def __init__(self, path_movies, path_ratings):
        self.path_movies = path_movies
        self.path_ratings = path_ratings
        self.movie_rating_thres = 0
        self.user_rating_thres = 0

    def set_filter_params(self, movie_rating_thres, user_rating_thres):
        self.movie_rating_thres = movie_rating_thres
        self.user_rating_thres = user_rating_thres

    def _prep_data(self):
        # Load movie and ratings data
        movies_df = pd.read_csv(os.path.join(self.path_movies))
        ratings_df = pd.read_csv(os.path.join(self.path_ratings))

        # Transform genres to vector
        all_genres = sorted(list(set('|'.join(list(movies_df['genres'])).split('|'))))
        movies_df['genre_vector'] = movies_df['genres'].apply(lambda x: self._genres_to_vector(x, all_genres))

        # Merge the movies and ratings dataframes
        merged_df = pd.merge(ratings_df, movies_df, on='movieId')

        # Compute weighted genre vectors
        merged_df['weighted_genre_vector'] = merged_df.apply(lambda x: x['genre_vector'] * x['rating'], axis=1)

        # Create user profiles
        user_profiles = merged_df.groupby('userId')['weighted_genre_vector'].apply(lambda x: np.mean(x, axis=0))

        return user_profiles, merged_df, movies_df

    def _genres_to_vector(self, genres, all_genres):
        genre_list = genres.split('|')
        return np.array([1 if genre in genre_list else 0 for genre in all_genres])

    def cosine_compute(self, user_profiles):
        # Calculate cosine similarity between users
        user_similarities = cosine_similarity(user_profiles)
        user_similarities_df = pd.DataFrame(user_similarities, index=user_profiles.index, columns=user_profiles.index)
        return user_similarities_df

    def make_recommendations(self, user_id, n_recommendations):
        recommendations = []
        user_profiles, merged_df, movies_df = self._prep_data()
        
        # Calculate user-content similarity
        user_similarities_df = self.cosine_compute(user_profiles)

        # Find movies user hasn't rated yet
        user_rated_movies = merged_df[merged_df['userId'] == user_id]['movieId']
        unrated_movies = movies_df[~movies_df['movieId'].isin(user_rated_movies)]

        # Predict ratings for unrated movies
        for _, row in unrated_movies.iterrows():
            predicted_rating = np.dot(user_similarities_df.loc[user_id], user_profiles.loc[:, row['genre_vector']]) / np.sum(user_similarities_df.loc[user_id])
            recommendations.append((row['movieId'], predicted_rating))

        # Sort recommendations by predicted rating
        recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)

        # Get movie titles for recommendations
        movie_titles = movies_df[movies_df['movieId'].isin([r[0] for r in recommendations])]['title'].values

        return movie_titles[:n_recommendations]

# Utilisation
cbf = ContentBasedFiltering('movies.csv', 'ratings.csv')
cbf.set_filter_params(50, 50)  # Vous pouvez ajuster ces seuils selon vos besoins
recommendations = cbf.make_recommendations(user_id=1, n_recommendations=10)
print(recommendations)
