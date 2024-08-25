import pandas as pd
import math
import numpy as np

global matrix
global similarity_matrix



def load_matrix(data):
    global matrix
    global similarity_matrix

    matrix = data
    pearson_similarity()

def pearson_similarity():

    global similarity_matrix

    ret = pd.DataFrame(columns=matrix.index, index=matrix.index,dtype=float)

    for i in range(len(ret.index)):
        for j in range(i, len(ret.index),1):

            left = ret.index[i]
            right = ret.index[j]
            left_avg = matrix.loc[left].replace(0, np.nan).mean()
            right_avg = matrix.loc[right].replace(0, np.nan).mean()
            left_op_sum = 0
            right_op_sum = 0
            mult_sum = 0

            for k in range(len(matrix.columns)):
                
                item = matrix.columns[k]
                if(matrix[item][left] != 0 and matrix[item][right]!=0):
                    left_op= matrix[item][left] - left_avg
                    right_op= matrix[item][right] - right_avg
                    left_op_sum += pow(left_op,2)
                    right_op_sum += pow(right_op,2)
                    mult_sum += left_op * right_op
            value = mult_sum / (math.sqrt(left_op_sum) * math.sqrt(right_op_sum))
            ret.loc[left, right] = value
            ret.loc[right, left] = value

    similarity_matrix = ret

def get_top_k_neighbors(user, k):
    similar_users = similarity_matrix[user].drop(user).nlargest(k).index
    return similar_users

def predict_rating(user, item, k):

    weighted_sum = 0
    sim_sum = 0
    neighbors = get_top_k_neighbors(user,k)
    user_avg_rating = matrix.loc[user].mean()

    for neighbor in neighbors:
        if pd.notna(matrix.loc[neighbor, item]):
            neighbor_avg_rating = matrix.loc[neighbor].mean()
            sim = similarity_matrix.loc[user, neighbor]
            weighted_sum += sim * (matrix.loc[neighbor, item] - neighbor_avg_rating)
            sim_sum += abs(sim)
    if sim_sum == 0:
        return user_avg_rating
    else:
        return user_avg_rating + weighted_sum / sim_sum