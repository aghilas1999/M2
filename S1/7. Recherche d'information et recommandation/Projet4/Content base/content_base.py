import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# AGHILAS SMAIL

class ContentRecommendation:
    def __init__(self, path_movies, path_ratings):
    
        self.path_movies = path_movies
        self.path_ratings = path_ratings

   
   

    # Une fonction de préparation des données que nous allons utiliser dans la recommandation.
    def _prep_data(self):
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
        genres_one_hot = genres_one_hot.apply(lambda x: x.map(lambda x: 1 if x != 0.0 else 0))

        # Concatenate one-hot encoded genres with the merged dataframe
        df_final = pd.merge(df_merged.drop('genres', axis=1), genres_one_hot, left_on='movieId', right_index=True)
        df_final.drop_duplicates(subset='movieId', inplace=True)
        print('test est passé')
        df_final1 = df_final.reset_index(drop=True)
        
        return df_final1
    
    
    
    
    
    '''Def calcul similarity'''
    def _genre_similarity(self, movies_with_ratings, movies_without_ratings): 
       
        similarity = cosine_similarity(movies_without_ratings,movies_with_ratings)
        return similarity
        
        
        
        
    def make_genre_recommendations(self, user_id, n_recommendations):
        
        df_final = self._prep_data()

        #Récupérer les genres des films que l'utilisateur a regardés
        user_genre = df_final[df_final['userId'] == user_id].drop(['userId'], axis=1).squeeze()
        
        # Récupérer les films qui ont les mêmes genres que ceux que l'utilisateur a regardés
        genre_movies = df_final[df_final['userId'] != user_id].drop(['userId'], axis=1).squeeze()
        
        print("Colonnes dans genre_movies :", genre_movies.shape)
        print("Colonnes dans user_genre :", user_genre.shape)

        # Calculer la similarité des genres
        similarity_matrix = self._genre_similarity(user_genre.drop(['movieId','rating'], axis=1), genre_movies.drop(['movieId','rating'], axis=1))
        mean_ratings = user_genre['rating'].mean()
        i = 0
        for index, movie in genre_movies.iterrows():
        # Obtenir les films non visionnés par l'utilisateur
                similarities = similarity_matrix[i]
                weighted_sum = 0
                similarity_sum = 0
                j=0
                for idx , g in user_genre.iterrows():
                    # print(user_genre['rating'].at())
                    weighted_sum += similarities[j] * (g['rating'] - mean_ratings)
                    similarity_sum += abs(similarities[j])
                    j += 1
               
                predicted_rating = mean_ratings + (weighted_sum / similarity_sum if similarity_sum != 0 else 0)
                genre_movies.at[index, 'rating'] = predicted_rating
                i += 1
        # Trier les films non visionnés en fonction de la similarité
        df_trie = genre_movies.sort_values(by='rating', ascending=False)

        top_recommendations = df_trie.head(n_recommendations)

        return top_recommendations
    
    
    
    

content_recommender = ContentRecommendation(path_movies="movies.csv", path_ratings="ratings.csv")

user_id = 1  # L'ID de l'utilisateur pour lequel vous voulez des recommandations
n_recommendations = 10  # Le nombre de recommandations que vous voulez

# Obtenir les recommandations
recommendations = content_recommender.make_genre_recommendations(user_id, n_recommendations)

# Afficher les recommandations
print(f"Top {n_recommendations} Recommendations for User {user_id}:")
for index, movie in recommendations.iterrows():
    print(f"Movie ID: {movie['movieId']}, Predicted Rating: {movie['rating']}")
