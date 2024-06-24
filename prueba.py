import numpy as np
import pandas as pd

# Ejemplo de dataset de ratings
data = {'user': ['Alice', 'Alice', 'Alice', 'Alice', 'Bob', 'Bob', 'Bob', 'Bob', 'Bob', 'Carol', 'Carol', 'Carol', 'Carol', 'Carol', 'Dave', 'Dave', 'Dave', 'Dave', 'Dave'],
        'item': ['Item1', 'Item2', 'Item3', 'Item4', 'Item1', 'Item2', 'Item3', 'Item4', 'Item5', 'Item1', 'Item2', 'Item3', 'Item4', 'Item5', 'Item1', 'Item2', 'Item3', 'Item4', 'Item5'],
        'rating': [5, 3, 4, 4, 3, 1, 2, 3, 3, 4, 3, 4, 3, 5, 3, 3, 1, 5, 4]}
ratings_df = pd.DataFrame(data)

# Crear la matriz de ratings
ratings_matrix = ratings_df.pivot(index='user', columns='item', values='rating')

# Aplicar Frecuencia Inversa de Usuario (IUF)
def apply_iuf(ratings_matrix):
    user_count = len(ratings_matrix.index)
    item_counts = ratings_matrix.notna().sum(axis=0)
    iuf = np.log(user_count / item_counts)
    return ratings_matrix * iuf

iuf_ratings_matrix = apply_iuf(ratings_matrix)

# Función para calcular la similitud de Pearson con IUF
def pearson_similarity_with_iuf(user_ratings):
    similarity_matrix = user_ratings.T.corr(method='pearson')
    return similarity_matrix

# Obtener la matriz de similitud ajustada por IUF
similarity_matrix_iuf = pearson_similarity_with_iuf(iuf_ratings_matrix)

# Selección de vecinos más cercanos (k=2 en este ejemplo)
def get_top_k_neighbors(similarity_matrix, user, k):
    similar_users = similarity_matrix[user].drop(user).nlargest(k).index
    return similar_users

# Obtener los vecinos más cercanos para Alice
top_neighbors_iuf = get_top_k_neighbors(similarity_matrix_iuf, 'Alice', 2)

print("Vecinos más cercanos de Alice (con IUF):")
print(top_neighbors_iuf)

# Función para predecir la calificación de un ítem para un usuario con IUF
def predict_rating_with_iuf(user, item, k):
    neighbors = get_top_k_neighbors(similarity_matrix_iuf, user, k)
    user_avg_rating = ratings_matrix.loc[user].mean()
    weighted_sum = 0
    sim_sum = 0
    for neighbor in neighbors:
        if pd.notna(ratings_matrix.loc[neighbor, item]):
            neighbor_avg_rating = ratings_matrix.loc[neighbor].mean()
            sim = similarity_matrix_iuf.loc[user, neighbor]
            weighted_sum += sim * (ratings_matrix.loc[neighbor, item] - neighbor_avg_rating)
            sim_sum += abs(sim)
    if sim_sum == 0:
        return user_avg_rating
    else:
        return user_avg_rating + weighted_sum / sim_sum

# Predecir la calificación de Alice para el Item5 con IUF
predicted_rating_iuf = predict_rating_with_iuf('Alice', 'Item5', 2)
print(f"Calificación predicha para Alice en Item5 (con IUF): {predicted_rating_iuf}")
