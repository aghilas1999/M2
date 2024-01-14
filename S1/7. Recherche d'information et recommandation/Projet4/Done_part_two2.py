import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from IPython.display import display
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD



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
    '''Def Prepa Done'''
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
        genres_one_hot = genres_one_hot.apply(lambda x: x.map(lambda x: 1 if x != 0.0 else 0))

        # Concatenate one-hot encoded genres with the merged dataframe
        df_final = pd.merge(df_merged.drop('genres', axis=1), genres_one_hot, left_on='movieId', right_index=True)

        # Pivot and create movie-user matrix with one-hot encoded genres
        # df_final = df_final.pivot_table(
        #     index='movieId', columns='userId', values='rating').fillna(0)
        print('test est passé')
        df_final1 = df_final.reset_index(drop=True)
        
        return df_final1
    
    
    
    
    
    '''Def calcul similarity'''
    def _genre_similarity(self, user_id, df): 
        # Récupérer les genres des films que l'utilisateur a regardés
        user_genres = df[df['userId'] == user_id].drop(['userId'], axis=1).squeeze()
        
        # Récupérer les films qui ont les mêmes genres que ceux que l'utilisateur a regardés
        similar_genre_movies = df[df['userId'] != user_id].drop(['userId'], axis=1).squeeze()

    
        display(user_genres)
        display(similar_genre_movies)
        similarity = cosine_similarity(user_genres,similar_genre_movies)
        # similar_movies_indices = np.argsort(similarity[0])[::-1]
        return similarity
        # print("Dimensions de user_genres avant reshape:", user_genres.shape)
        # user_genres_reshaped = user_genres.values
        # print("Dimensions de user_genres après reshape:", user_genres_reshaped.shape)

        # print("Dimensions de all_genres avant reshape:", all_genres.shape)
        # all_genres_reshaped = all_genres.values
        # print("Dimensions de all_genres après reshape:", all_genres_reshaped.shape)
        
        # # Réduire la dimensionnalité avec Truncated SVD
        # # svd = TruncatedSVD(n_components=50)
        # # user_genres_reduced = svd.fit_transform(user_genres_reshaped)
        # # all_genres_reduced = svd.transform(all_genres_reshaped)
        # # Calculez la similarité cosinus
        # cosine_sim = cosine_similarity(user_genres_reshaped, all_genres_reshaped)

        # user_similarity.append(cosine_sim)

        # user_similarity = np.array(user_similarity)
        # return user_genres, all_genres, user_similarity






    def make_genre_recommendations(self, user_id, n_recommendations):
        """
        Fait des recommandations basées sur les genres pour un utilisateur donné.
        """
        # Obtenir les données à partir de _prep_data.
        df_final = self._prep_data()

        # Calculer la similarité entre les genres
        genre_similarity = self._genre_similarity(user_id, df_final)

        # Sélectionner les films non regardés par l'utilisateur
        unwatched_movies = df_final.loc[(df_final['userId'] == user_id) & df_final['rating'].isnull()]

        recommendations = []

        for movie_id, row in unwatched_movies.iterrows():
            similarity_sum = 0
            weighted_rating_sum = 0
            movie_genres = row.drop(['index', 'userId', 'movieId', 'rating'])

            for genre_index, genre in enumerate(all_genres.columns):
                if movie_genres[genre] > 0:  # Le film a ce genre
                    similarity = genre_similarity[0][genre_index]
                    weighted_rating_sum += similarity
                    similarity_sum += np.abs(similarity)

            if similarity_sum > 0:
                user_mean_rating = np.mean(df_final[user_id][df_final[user_id] != 0])
                predicted_rating = user_mean_rating + (weighted_rating_sum / similarity_sum)
                recommendations.append((movie_id, predicted_rating))

                print("movie : ", movie_id, "predicted rating : ", predicted_rating)

        # Trier les recommandations par rating prédit
        recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)

        # Renvoyer les IDs des films recommandés
        return [movie_id for movie_id, _ in recommendations[:n_recommendations]]

  
# # Exemple d'utilisation
# recommender = ContentRecommendation('movies.csv', 'ratings.csv')
# user_id = 1  # Remplacez cela par l'ID de l'utilisateur que vous souhaitez tester
# n_recommendations = 5

# genre_recommendations = recommender.make_genre_recommendations(user_id, n_recommendations)
# print("Genre Recommendations:", genre_recommendations)
        
        
# Create an instance of ContentRecommendation
recommendation_system = ContentRecommendation(path_movies='movies.csv', path_ratings='ratings.csv')

# Prepare data using the _prep_data method
df_final = recommendation_system._prep_data()

# Choose a user_id for testing (replace it with an actual user_id from your dataset)
user_id_to_test = 1

# Call the _genre_similarity method
user_genres = recommendation_system._genre_similarity(user_id=user_id_to_test, df=df_final)

# Print or display the result
print(user_genres)

# # # Exemple d'utilisation   
# recommender = ContentRecommendation('movies.csv', 'ratings.csv')
# df_final = recommender._prep_data()  # Assurez-vous d'avoir les données préparées
# display(df_final)
# df_final.to_csv('test.csv',index=False)
# user_id = 1  # Remplacez cela par l'ID de l'utilisateur que vous souhaitez tester

# user_genres, all_genres, genre_similarity = recommender._genre_similarity(user_id,df_final)

# Affichez les résultats
# print("Genres de l'utilisateur:")
# print(user_genres)
# print("\nTous les genres:")
# print(all_genres)
# print("\nSimilarités de genre:")
#print(genre_similarity)
# display(genre_similarity)
# # Flatten the 3D array
# flattened_similarity = genre_similarity.flatten()

# # Save flattened_similarity to TXT
# np.savetxt('genre_similarity.txt', flattened_similarity, delimiter='\t')
#   # def _content_based_user_similarity(self, df_final, user_id):
            
    #     """
    #     Calcule la similarité entre les utilisateurs en utilisant la similarité cosinus basée sur le contenu (genres des films).

    #     Parameters
    #     ----------
    #     df_final : pandas DataFrame, matrice utilisateur-genre (binaire)

    #     user_id : int, ID de l'utilisateur pour lequel on veut calculer la similarité

    #     Returns
    #     -------
    #     numpy array, matrice de similarité entre l'utilisateur et les autres
    #     """
        
    #     user_similarity = []  # Initialisez la liste pour stocker les similarités

    #     for suser in df_final.index:
    #         # Récupérez les genres regardés par l'utilisateur et l'utilisateur similaire
    #         genres_user = df_final.loc[user_id]
    #         genres_suser = df_final.loc[suser]

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
    
'''
 def make_genre_recommendations(self, user_id, n_recommendations):
        """
        Fait des recommendation basée sur les genre pour un utilisateur donné.
        """
        # get data frome _prep_data.
        df_final = self._prep_data()
        print("Type de df_final avant l'appel à _genre_similarity:", type(df_final))
        # trouve les utilisateurs similaires
        # calcule la similarité entre les genres
        user_genres, all_genres,genre_similarity = self._genre_similarity(df_final,user_id)
        
        similar_genres = np.argsort(genre_similarity)[::-1][1:] + 1  

        # trouvez les genres similaires
        # user_genres, all_genres, genre_similarity = self._genre_similarity(user_id, df_final)
        #trouvez les genres non regarder par l'utilisateur
        unwatched_movies = df_final[(df_final['userId'] == user_id) & (df_final['movieId'].isnull())]

        recommendations = []
        
        for movie_id in unwatched_movies.index: 
            similarity_sum = 0
            weighted_rating_sum = 0 
            
            for similar_genre in similar_genres:
                if df_final[similar_genre][movie_id] > 0: # Le film a ce genre
                    similarity_genre = np.mean(df_final[similar_genre][df_final[similar_genre] != 0])
                    similarity = genre_similarity[similar_genre - 1 ]
                    weighted_rating_sum +=similarity * (df_final[similar_genre][movie_id] - similarity_genre)
                    similarity_sum += np.abs(similarity)
                    
            if similarity_sum > 0:
                user_mean_rating = np.mean(df_final[user_id][df_final[user_id] != 0])
                predicted_rating = user_mean_rating + (weighted_rating_sum / similarity_sum)
                recommendations.append((movie_id, predicted_rating))
                
                print("movie : ", movie_id, "predicted rating : ", predicted_rating)
        # trie les recommandations par rating prédit
        recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)
        
         # Afficher les IDs des films recommandés
        recommended_movie_ids = [movie_id for movie_id, _ in recommendations[:n_recommendations]]
        print("IDs des films recommandés:", recommended_movie_ids)

        # Renvoyer les IDs des films recommandés
        return recommended_movie_ids
        '''