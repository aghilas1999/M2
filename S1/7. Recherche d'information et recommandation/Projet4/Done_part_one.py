import pandas as pd
import numpy as np
'''
Travaille fait par SMAIL Aghilas
'''
# Chargez les données.
movies_dataframe = pd.read_csv("movies.csv")
ratings_dataframe = pd.read_csv("ratings.csv")

def pearson_similarity(rat1, rat2):
    # Rejoignez les évaluations des deux utilisateurs
    merg = rat1.join(rat2, lsuffix="_user1", rsuffix="_user2")
    
    if len(merg) == 0:
            return 0 
 
    # Calculez la moyenne
    moy_user1 = rat1['rating'].mean()
    moy_user2 = rat2['rating'].mean()

    # Calculez la similarité de Pearson
    numerator = ((merg['rating_user1'] - moy_user1) * (merg['rating_user2'] - moy_user2)).sum()
    denominator_user1 = np.sqrt(((merg['rating_user1'] - moy_user1) ** 2).sum())
    denominator_user2 = np.sqrt(((merg['rating_user2'] - moy_user2) ** 2).sum())
    denominator = (denominator_user1 * denominator_user2)

    if denominator == 0:
        return 0  # Évitez la division par zéro

    similarity = numerator / denominator
    return similarity

# Fonction pour caculer la distance entre l'utilisateur ciblé et les autres utilisateurs
def find_user_distance(userId1, userId2):
    user_ratings1 = find_user_ratings(userId1)
    user_ratings2 = find_user_ratings(userId2)
    
    similarity = pearson_similarity(user_ratings1, user_ratings2)
    
    return [userId1, userId2, similarity]

# Fonction pour avoir les films que l'utilisateur a donnée un avis
def find_user_ratings(userID):
    user_ratings = ratings_dataframe.query(f"userId == {userID}")
    return user_ratings[["movieId", "rating"]].set_index("movieId")

# Avoir la distance entre l'utilisateur ciblé et le reste des utilisateurs
def find_relative_distance(userId):
    users = ratings_dataframe["userId"].unique()
    users = users[users != userId]
    distances = [find_user_distance(userId, every_other_user_id) for every_other_user_id in users]
    
    return pd.DataFrame(distances, columns=["masterUserId", "userId", "similarity"])

# Avoir les utilsiateur qui ont la plus grand similarity avec l'utilisateur ciblé
def find_closest_users(userId, number_of_users):
    relative_distances = find_relative_distance(userId)
    relative_distances.sort_values("similarity", ascending=False, inplace=True)
    return relative_distances.head(number_of_users)

#Avoir la similarity la plus basse
def find_least_similar_user(userId):
    users = ratings_dataframe["userId"].unique()
    users = users[users != userId]
    
    min_similarity = float('inf')  
    least_similar_user = None  
    
    for user_id in users:
        similarity = pearson_similarity(find_user_ratings(userId), find_user_ratings(user_id))
        if similarity < min_similarity:
            min_similarity = similarity
            least_similar_user = user_id
    
    return least_similar_user, min_similarity

#Fonction pour faire la recommendation
def make_recommendation(userId):
    user_ratings = find_user_ratings(userId)
    closest_users = find_closest_users(userId,10)
    most_similar_user_id = closest_users.iloc[0]["userId"]
    
    closest_user_ratings = find_user_ratings(most_similar_user_id)
    unwatched_movies = closest_user_ratings.drop(user_ratings.index, errors="ignore")
    
    unwatched_movies = unwatched_movies.sort_values("rating", ascending=False)
    #unwatched_movies = unwatched_movies.join(movies_dataframe)
    unwatched_movies = unwatched_movies.join(movies_dataframe.set_index('movieId'), on='movieId')
    return unwatched_movies.head(15)

while True:
    
    user_id_to_predict = int(input("Entrez le numéro de l'utilisateur que vous souhaitez prédire: "))
    if user_id_to_predict == -1:
        break  
    
    recommendations = make_recommendation(user_id_to_predict)
    
    print("Recommandations pour l'utilisateur", user_id_to_predict)
    print(recommendations)