
import pandas as pd
import math

global dataset
global loaded 
loaded = False

def load_dataset():
    global dataset
    global loaded
    dataset = pd.read_csv('dataset/matrix.csv')
    loaded = True
    

def get_items():
    try:
       x = dataset.columns
    except :
        return []
    return list(dataset.columns)

def get_load_state():
    return loaded

def ratings_matrix_creator(dataframe):
        return dataframe.pivot(index='user', columns='item', values='rating')

# Función para calcular la similitud de Pearson. 
def pearson_similarity(ratings_matrix, item_variances): 
    similarity_matrix = ratings_matrix.T.corr(method='pearson')
    
    return similarity_matrix

# Función para caluclar la similitud de Pearson a mano.
def pearson_similarity_long(rating_matrix):

    ret = pd.DataFrame(columns=rating_matrix.index, index=rating_matrix.index)

    for i in range(len(ret.index)):
        for j in range(i, len(ret.index),1):

            left = ret.index[i]
            right = ret.index[j]
            left_avg = rating_matrix.loc[left].mean()
            right_avg = rating_matrix.loc[right].mean()
            left_op_sum = 0
            right_op_sum = 0
            mult_sum = 0

            for k in range(len(rating_matrix.columns)):
                item = rating_matrix.columns[k]
                left_op= rating_matrix[item][left] - left_avg
                right_op= rating_matrix[item][right] - right_avg
                left_op_sum += pow(left_op,2)
                right_op_sum += pow(right_op,2)
                mult_sum += left_op * right_op
            value = mult_sum / (math.sqrt(left_op_sum) * math.sqrt(right_op_sum))
            ret.loc[left, right] = value
            ret.loc[right, left] = value

        

    return ret


# Selección de los k vecinos mas cercanoss
def get_top_k_neighbors(similarity_matrix, user, k):
    similar_users = similarity_matrix[user].drop(user).nlargest(k).index
    return similar_users

def items_variances(ratings_matrix):
    return ratings_matrix.var(axis=0, skipna=True)


# Función para predecir la calificación de un ítem para un usuario con ajuste por varianza
def predict_rating(user, item, k, ratings_matrix, similarity_matrix_var_adjusted, neighbors, user_avg_rating):

    # similarity_matrix_var_adjusted = pearson_similarity(ratings_matrix, items_variances(ratings_matrix))

    # neighbors = get_top_k_neighbors(similarity_matrix_var_adjusted, user, k)

    # user_avg_rating = ratings_matrix.loc[user].mean()

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
    
##### Método del Grafo #####

def get_liked_items(user, rating_matrix):

    liked_items = []

    matrix = rating_matrix.loc[user]

    for item in matrix.index:
        if  matrix[item]>= 3:
            liked_items.append(item)
    return liked_items

def get_related_users(liked_items, rating_matrix, user):

    related_users = []

    for item in liked_items:
        matrix = rating_matrix[item].index  
        for users in matrix:
            if users not in related_users and users!=user:
                related_users.append(users)
    return related_users

def get_posible_items(user,rating_matrix,amount):

    liked_items = get_liked_items(user,rating_matrix)
    related_users = get_related_users(liked_items,rating_matrix,user)
    
    posible_items=[]

    for users in related_users:
        matrix = rating_matrix.loc[users].index
        for item in matrix:
            if item not in liked_items and item not in posible_items and amount != 0:
                posible_items.append(item)
                amount = amount-1
    return posible_items

def get_potential_predictions(user, neigbours_amount, items_amount, rating_matrix):

    similarity_matrix = pearson_similarity(rating_matrix,5)

    neigbours = get_top_k_neighbors(similarity_matrix,user,neigbours_amount)

    user_avg_rating = rating_matrix.loc[user].mean()

    posible_items = get_posible_items(user, rating_matrix, items_amount)

    posible_items_rating = {}

    for item in posible_items:
        posible_items_rating[item] = predict_rating(user, item, neigbours_amount, rating_matrix, similarity_matrix, neigbours, user_avg_rating)

    return posible_items_rating



        