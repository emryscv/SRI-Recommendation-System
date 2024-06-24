
import pandas as pd

def ratings_matrix_creator(dataframe):
    return dataframe.pivot(index='user', columns='item', values='rating')

# Función para calcular la similitud de Pearson. 
def pearson_similarity(ratings_matrix, item_variances): 
    similarity_matrix = ratings_matrix.T.corr(method='pearson')
    

    return similarity_matrix

# Selección de los k vecinos mas cercanoss
def get_top_k_neighbors(similarity_matrix, user, k):
    similar_users = similarity_matrix[user].drop(user).nlargest(k).index
    return similar_users

def items_variances(ratings_matrix):
    return ratings_matrix.var(axis=0, skipna=True)


# Función para predecir la calificación de un ítem para un usuario con ajuste por varianza
def predict_rating(user, item, k, similarity_matrix_var_adjusted, ratings_matrix ):

    neighbors = get_top_k_neighbors(similarity_matrix_var_adjusted, user, k)

    user_avg_rating = ratings_matrix.loc[user].mean()

    weighted_sum = 0
    sim_sum = 0

    for neighbor in neighbors:
        if pd.notna(ratings_matrix.loc[neighbor, item]):
            neighbor_avg_rating = ratings_matrix.loc[neighbor].mean()
            sim = similarity_matrix_var_adjusted.loc[user, neighbor]
            weighted_sum += sim * (ratings_matrix.loc[neighbor, item] - neighbor_avg_rating)
            sim_sum += abs(sim)
    if sim_sum == 0:
        return user_avg_rating
    else:
        return user_avg_rating + weighted_sum / sim_sum
